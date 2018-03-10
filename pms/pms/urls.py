"""pms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import admin
import views

admin.autodiscover()

urlpatterns = [
    url(r'^$',lambda x: redirect(reverse('index'))),
    url(r'^admin/', admin.site.urls),
    url(r'^useraccount/',include('useraccount.urls')),
    url(r'^index/$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
]
