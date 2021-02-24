# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import ugettext_lazy as _

from django_auth.models import User


@admin.register(User)
class UserAdmin(_UserAdmin):
    def make_activate(self, request, queryset):
        queryset.update(is_active=True)
    make_activate.short_description = _("activate")

    def make_deactivate(self, request, queryset):
        for obj in queryset:
            obj.is_active = False
            obj.save()
            self.log_change(request, obj, '[{"changed": {"fields": ["is_active"]}}]')
    make_deactivate.short_description = _("deactivate")

    search_fields = ['username', 'mobile']
    list_display = ('username', 'mobile', 'email', 'is_active')
    list_filter = ('groups', 'is_staff', 'is_active')
    actions = ['make_deactivate', 'make_activate']
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': (
            'username', 'password', 'mobile', 'email'
        )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
