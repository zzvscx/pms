# -*- coding: utf-8 -*-


from django.conf.urls import include, url

from weixin.views import *
from weixin.weixinbase import handleRequest

urlpatterns=[
    url(r'^$', handleRequest),
    # url(r'^bind/$', wx_service_number_bind),
    ]
