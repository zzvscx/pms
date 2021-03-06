#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User, UserScore, UserMessage
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
                           'name', 'sex','password', 'team', 'term', 'intake', 'at_school', 'have_roll', 'roll_in_school',
                           'education','campus','desc')}),
        (u'权限', {'fields': ('is_active', 'is_staff', 'is_superuser',
                            'groups', 'user_permissions')}),
        (u'重要日期', {'fields': ('last_login', 'date_joined')}),
    ]

    list_display = ('stuId', 'username', 'team',
                    'intake', 'is_active', 'is_staff')
    search_fields = ('team', 'stuId', 'username')
    list_filter = ('is_staff', 'is_active')
    raw_id_fields = ('team',)


@admin.register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('user','course','midterm','final_exam','usual','experimental','retest','total_points')
    search_fields = ('user','course')
    raw_id_fields = ('user','course')

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('user','message_type','message')
    list_filter = ('message_type',)
    search_fields = ('user',)