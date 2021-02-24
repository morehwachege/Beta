# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six
from django.contrib.auth.models import User as _User
from django.contrib.auth.models import UserManager as _UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_auth.user_validators import UnicodeUsernameValidator, ASCIIUsernameValidator


class UserManager(_UserManager):
    def get_admin(self):
        super_user = User.objects.filter(is_superuser=1).first()
        return super_user

    def get_system_user(self):
        system = self.model.objects.filter(username='system').first()
        if not system:
            admin = self.get_admin()
            system = self.model.objects.filter(id=admin.id).first()
        return system

    def get_user(self, username=None, mobile=None):
        user = None
        if username:
            user = self.filter(username=username).first()
        elif mobile:
            user = self.filter(mobile=mobile).first()
        return user


class User(_User):
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    avatar_image = models.ImageField(
        upload_to='media/avatar/%Y/%m',
        verbose_name=_("avatar image"),
        default='media/images/user_avatar.jpg'
    )
    country_code = models.CharField(
        default='86',
        max_length=50,
        verbose_name=_("country code")
    )
    mobile = models.CharField(
        max_length=50,
        verbose_name=_("mobile")
    )

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("User Management")
