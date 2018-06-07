#-*- coding:utf-8 -*-
import requests
from django.shortcuts import render
from django.http import Http404, HttpResponse
from useraccount.models import User
from django.db.models import Q
from django.core.cache import cache
from .models import WeixinKey
# Create your views here.

def is_weixin_browser(request):
    r = re.compile('MicroMessenger', re.I)
    return r.search(request.META.get("HTTP_USER_AGENT", ""))


# def wx_service_number_bind(request):
#     # if not is_weixin_browser(request):
#     #     raise Http404

#     if request.method =='GET':
#         openid = request.session.get('fwh_openid')
#         if not openid:
#             wx_app = WeixinKey.objects.get(desc='FWH')
#             appid =  wx_app.appid
#             appsecret = wx_app.appsecret
#             code = request.GET.get('code')
#             url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code"
#             r = requests.get(url.format(appid, appsecret, code))
#             openid = r.json()['openid']
#             request.session['fwh_openid'] = openid
#         return render(request,'useraccount/login.html', {'source':'wxfwh'})
#     elif request.method == "POST":
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         if request.session.get('fwh_openid',''):
#             user = User.objects.filter(Q(username=username)|Q(stuId=username)).first()
#             if user:
#                 fwh_openid = request.session['fwh_openid']
#                 fwh_user = WeixinUser.objects.filter(openid=fwh_openid,subscribe=1).first()
#             if fwh_user:
#                 fwh_user.user = user
#                 fwh_user.desc = 'fwh_user'
#                 fwh_user.save()
#             else:
#                 fwh_user = WeixinUser(user=user, openid=fwh_openid,subscribe=1,desc='fwh_user')
#                 fwh_user.save()
#             fwh_user.notification_for_bind()
#             return render(request,'weixin/fwhbind_result.html',{'result':u'绑定成功'})
#     return render(request,'useraccount/login.html', {'source':'wxfwh', 'error_message': u'账号或密码错误，请重新登录！'})
        

