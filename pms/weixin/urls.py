# -*- coding: utf-8 -*-


from django.conf.urls import patterns, include, url

from weixin.views import *
from weixin.weixinbase import handleRequest

urlpatterns = patterns(\
    'weixin.views',
   )

urlpatterns += patterns(\
    '',
    url(r'^$', handleRequest),
    # url(r'^bind/$', wx_service_number_bind),
    )
