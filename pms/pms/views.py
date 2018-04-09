#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from useraccount.models import UserMessage

def index(request):
    return render(request,'pms/index.html')

def about(request):
    if request.method == 'POST':
        if not request.user:
            return render(request,'pms/about.html',{'msg':u'请登陆后进行反馈'})
        message_type = request.POST.get('message_type')
        message = request.POST.get('message')
        if not message:
            return render(request,'pms/about.html',{'msg':u'反馈信息不可为空'})
        if UserMessage.objects.create(user=request.user, message_type=message_type,message=message):
            return render(request,'pms/about.html',{'msg':u'反馈成功'})
    return render(request,'pms/about.html')
