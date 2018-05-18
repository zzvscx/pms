# -*- coding: utf-8 -*- 
import urllib2
import json

from django.contrib import admin
from weixin.models import WeixinUser, WeixinKey

class BindWeixinUserFilter(admin.SimpleListFilter):
    title = u'已绑定用户'
    parameter_name = 'bind_user'
    # template = "admin/filter_form.html"
    params = [(u'true', '是')]

    def lookups(self, request, model_admin):
        return self.params

    def queryset(self, request, queryset):
        value = request.GET.get('bind_user')
        if value is None:
            return queryset
        elif value == 'true':
            return queryset.exclude(user=None)


class WeixinUserAdmin(admin.ModelAdmin):

    list_filter = (BindWeixinUserFilter,'last_modified_time','create_time')
    raw_id_fields = ('user', )
    search_fields = ('user__username', 'openid')
    list_display = ("openid", "user", "subscribe", "create_time", "last_modified_time")
    readonly_fields = ("create_time","last_modified_time")

class WeixinKeyAdmin(admin.ModelAdmin):

    readonly_fields = ("create_time","last_modified_time")
    list_display = ("appid", "appsecret", "token")
    actions = ['update_menu']
    
    def update_menu(self, request, queryset):
        url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"
        for x in queryset:
            data = urllib2.urlopen(url % x.token, data = str(x.menu)).read()
            self.message_user(request, data)

admin.site.register(WeixinUser, WeixinUserAdmin)
admin.site.register(WeixinKey, WeixinKeyAdmin)
