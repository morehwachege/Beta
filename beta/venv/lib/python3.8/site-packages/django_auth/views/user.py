# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import HttpResponse
from django.template import loader
from django.views.generic import View


class UserHomeIndexView(View):
    def get(self, request):
        template = loader.get_template('django_auth/home/index.html')
        return HttpResponse(template.render({}, request))


class UserLoginView(View):
    def get(self, request):
        template = loader.get_template('django_auth/user/login.html')
        return HttpResponse(template.render({}, request))


class UserRegisterView(View):
    def get(self, request):
        template = loader.get_template('django_auth/user/register.html')
        return HttpResponse(template.render({}, request))


class UserLogoutView(View):
    def get(self, request):
        template = loader.get_template('django_auth/user/logout.html')
        return HttpResponse(template.render({}, request))
