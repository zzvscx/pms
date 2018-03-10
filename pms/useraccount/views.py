#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User
# Create your views here.

class StudentBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)| Q(stuId=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

def login(request):
    return HttpResponse(u'登录成功')
