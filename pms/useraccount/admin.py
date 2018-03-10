#-*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = [
        (None, {'fields': ('stuId','username','password')}),
        (u'权限', {'fields': ('is_active','is_staff','is_superuser',
                        'groups','user_permissions')}),
        (u'重要日期',{'fields': ('last_login','date_joined')}),
    ]

    list_display = ('stuId','username','is_active','is_staff')
    search_fields = ('stuId','username')
    list_filter = ('is_staff','is_active')