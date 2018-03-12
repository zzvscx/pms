#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib import auth
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

    if request.user.is_authenticated(): 
        return HttpResponseRedirect('/index/')
    
    if request.method == 'GET':
        return render(request,'useraccount/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/index/')
        else:
            return render(request,'useraccount/login.html',{'error_message':'账号或密码错误，请重新登录！'}) 

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')