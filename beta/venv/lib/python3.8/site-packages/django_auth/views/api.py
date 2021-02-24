# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re
import sys
import time
import uuid
from datetime import datetime
from random import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from django_auth.models import User
from django_auth.views.base import api_common

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass
except Exception as err:
    raise err

# Warning! don't change!
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(phone_numbers, template_code, template_param=None):
    business_id = uuid.uuid1()
    sign_name = settings.SMS_SIGN
    smsRequest = SendSmsRequest.SendSmsRequest()
    smsRequest.set_TemplateCode(template_code)
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    smsRequest.set_OutId(business_id)
    smsRequest.set_SignName(sign_name)
    smsRequest.set_PhoneNumbers(phone_numbers)
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    return smsResponse


def generate_code():
    return int(1000 + random() * 8999)


class APIVerificationCodeView(View):

    def post(self, request):
        country_code = request.POST.get('country_code', '')
        mobile = request.POST.get('mobile', '')
        type = request.POST.get('type', '')

        if country_code:
            find_lst = re.findall("\d+\.?\d*", country_code)
            country_code = str([int(item) for item in find_lst][0])

        verfication_code_req_time = request.session.get('verfication_code_req_time', 0)
        if verfication_code_req_time + 60 >= time.time():
            response = api_common({}, -6, 'Only can get one verify code every 60 seconds')
            return JsonResponse(response)

        if type == 'forgetpasswd' or type == 'login':
            user = User.objects.filter(mobile=mobile).first()
            if not user:
                response = api_common({}, -3, 'User not exist')
                return JsonResponse(response)
            country_code = user.country_code
        elif type == 'register':
            user = User.objects.filter(mobile=mobile).first()
            if user:
                response = api_common({}, -4, 'Mobile has been registered')
                return JsonResponse(response)

        if type == 'login':
            if country_code == '86':
                tpl_id = settings.SMS_TPL_LOGIN_CN_ID
            else:
                mobile = '00' + country_code + mobile
                tpl_id = settings.SMS_TPL_LOGIN_FOREIGN_ID
        elif type == 'forgetpasswd':
            if country_code == '86':
                tpl_id = settings.SMS_TPL_FORGETPASSWD_CN_ID
            else:
                mobile = '00' + country_code + mobile
                tpl_id = settings.SMS_TPL_FORGETPASSWD_FOREIGN_ID
        elif type == 'register':
            if country_code == '86':
                tpl_id = settings.SMS_TPL_REGISTER_CN_ID
            else:
                mobile = '00' + country_code + mobile
                tpl_id = settings.SMS_TPL_REGISTER_FOREIGN_ID
        else:
            response = api_common({}, -5, 'Incorrect verify code type')
            return JsonResponse(response)

        code = generate_code()
        request.session['verfication_code'] = code
        request.session['verfication_code_req_time'] = time.time()

        if settings.SMS_SIGN:
            result = send_sms(mobile, tpl_id, "{\"code\":\"" + str(code) + "\"}")
            result_obj = json.loads(result)
            print(result, mobile, country_code, country_code == '86', tpl_id)
            if result_obj['Code'] == "OK":
                response = api_common({}, 0, 'success')
                return JsonResponse(response)
            else:
                response = api_common({}, -1, result_obj['Message'])
                return JsonResponse(response)
        else:
            response = api_common({}, -2, 'Please config sms in django settings first!')
            return JsonResponse(response)


class APIUserLoginView(View):
    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        mobilecode = request.POST.get('mobilecode', '')
        keepLogin = request.POST.get('keepLogin', '')

        if mobilecode and mobilecode is not None and mobilecode != '':
            # mobile + code
            verfication_code = request.session.get('verfication_code', '')
            request.session['verfication_code'] = ''
            if settings.DEBUG or (verfication_code and str(verfication_code) == str(mobilecode)):
                user = User.objects.get_user(mobile=username)
                if user is None:
                    response = api_common({}, -1, _("User not exist"))
                    return JsonResponse(response)
            else:
                response = api_common({}, -2, _("Incorrect code"))
                return JsonResponse(response)
        else:
            # username/mobile + password
            user = User.objects.get_user(username=username)
            wrong_passwd = False
            if user:
                # username + password
                user = authenticate(username=username, password=password)
                if not user:
                    wrong_passwd = True
            else:
                # mobile + password
                user = User.objects.get_user(mobile=username)
                if user:
                    user = authenticate(username=user.username, password=password)
                    if not user:
                        wrong_passwd = True
            if user and not user.is_active:
                response = api_common({}, -3, _("User banned"))
                return JsonResponse(response)
            if wrong_passwd:
                response = api_common({}, -4, _("Incorrect password"))
                return JsonResponse(response)

        if user and user.is_active:
            login(request, user)
            if keepLogin == 'true':
                request.session.set_expiry(datetime.today().year + 1)
            response = api_common({})
            return JsonResponse(response)
        else:
            response = api_common({}, -5, _("User not exist"))
            return JsonResponse(response)


class APIUserLogoutView(View):
    def post(self, request):
        if request.user.is_authenticated():
            logout(request)
        response = api_common({})
        return JsonResponse(response)


class APIUserRegisterView(View):
    def is_valid(self, str):
        for i in str:
            if i in ['\'', '"', '\\']:
                return 0
        return 1

    def post(self, request):
        country_code = request.POST.get('country_code', '')
        mobile = request.POST.get('mobile', '')
        mobilecode = request.POST.get('mobilecode', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if country_code:
            find_lst = re.findall("\d+\.?\d*", country_code)
            country_code = str([int(item) for item in find_lst][0])

        verfication_code = request.session.get('verfication_code', '')
        request.session['verfication_code'] = ''

        if settings.DEBUG or (verfication_code and str(verfication_code) == str(mobilecode)):
            if not self.is_valid(username):
                response = api_common({}, -1, _("Incorrect username"))
                return JsonResponse(response)
            if not self.is_valid(password):
                response = api_common({}, -2, _("Incorrect password"))
                return JsonResponse(response)

            user = User.objects.filter(mobile=mobile).first()
            if user:
                response = api_common({}, -3, _("Mobile has been registered"))
                return JsonResponse(response)

            user = User.objects.filter(username=username).first()
            if user:
                response = api_common({}, -4, _("Username has been registered"))
                return JsonResponse(response)

            user = User.objects.create_user(username=username, email=None, password=password)
            user.country_code = country_code
            user.mobile = mobile
            user.save()

            # Login after registered
            login(request, user)
            request.session.set_expiry(datetime.today().year + 1)

            response = api_common({})
            return JsonResponse(response)
        else:
            response = api_common({}, -5, _("Incorrect code"))
            return JsonResponse(response)
