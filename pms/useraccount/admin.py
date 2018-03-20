#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User, UserScore
from django import forms
from django.contrib.auth.forms import UserChangeForm

class UserChangeForm(UserChangeForm):
    username = forms.CharField(max_length=36)

    class Meta:
        model = User
        fields = '__all__'

    def clean_username(self):
        return self.cleaned_data.get('username')


@admin.register(User)
class UserAdmin(UserAdmin):

    form = UserChangeForm
    fieldsets = [
        (None, {'fields': ('stuId', 'username',
                           'name', 'password', 'team', 'intake')}),
        (u'权限', {'fields': ('is_active', 'is_staff', 'is_superuser',
                            'groups', 'user_permissions')}),
        (u'重要日期', {'fields': ('last_login', 'date_joined')}),
    ]

    list_display = ('stuId', 'username', 'team',
                    'intake', 'is_active', 'is_staff')
    search_fields = ('team', 'stuId', 'username')
    list_filter = ('is_staff', 'is_active')
    raw_id_fields = ('team',)
