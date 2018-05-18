#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from useraccount.models import User
import urllib2
import json
import requests
from django.core.cache import cache

# Create your models here.


class WeixinUser(models.Model):

    user = models.ForeignKey(User, null=True, blank=True)
    openid = models.CharField(max_length = 64)
    subscribe = models.BooleanField(default=False,blank=True)
    desc = models.CharField(max_length = 10, default = '')
    create_time = models.DateTimeField(verbose_name=u"创建时间",auto_now_add=True,null=True,editable=True,)
    last_modified_time = models.DateTimeField(editable=True,verbose_name=u"最后修改时间",auto_now=True,null=True)

    def notification_to_wxuser(self, template_id, data={}, url='', topcolor='',**kwargs):
        openid = self.openid
        service_number = WeixinKey.objects.get(desc='fwh')
        appid = service_number.appid
        appsecret = service_number.appsecret
        access_token = service_number.token
        post_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
        post_data = {
            "touser": openid,
            "template_id": template_id,
            "url": url,
            "topcolor": topcolor,
            "data": data,
        }
        post_data = json.dumps(post_data)
        r = requests.post(post_url,data=post_data)
        errcode = r.json()['errcode']
        errmsg = r.json()['errmsg']
        if str(errcode) == '43004':
                self.user = None
                self.save()
    
    def notification_for_userscore(self,userscore):
        template_id = 'CgCZesvkbiBLTD169XVQaMK3e3BPWftUUuTvDtvY2IY'
        url = ''
        data = {
            'title': {         # 提醒
                'value': u'您的{}成绩已更新'.format(userscore.course.name),
                'color': '#173177'
            },
            'username': {      # 用户姓名
                'value': userscore.user.name + ' ' + userscore.user.username,
                'color': '#173177'
            },
            'stuid': {     
                'value': str(userscore.user.stuId),
                'color': '#173177'
            },
            'score': {    
                'value': str(userscore.total_score),
                'color': '#173177'
            },
            'points': { 
                'value': str(userscore.points),
                'color': '#173177'
            },
            'remark':{
                'value': u'如发现成绩错误，请登录长安大学学生成绩管理系统提交反馈，管理员会在一至三个工作日内进行审核和修复。',
                'color': '#FF0000'
            }
        }
        self.notification_to_wxuser(template_id, data, url)
        
    def notification_for_bind(self):
        template_id = 'OdQyQOrPXKWabH02uVZSCDOHZbwc75eaY8J8F5jgTYU'
        url = ''
        data = {
            'first': {           #提醒
                'value': '您已经绑定长安大学学生成绩管理系统',
                'color': '#173177'
            },
            'keyword1': {        #账号
                'value': self.user.username + ' ' + str(self.user.stuId),
                'color': '#173177'
            },
            'keyword2': {        #绑定时间
                'value': self.last_modified_time.strftime("%Y/%m/%d %H:%M:%S"),
                'color': '#173177'
            },
            'remark': {          
                'value': u'如发现成绩错误，请登录长安大学学生成绩管理系统提交反馈，管理员会在一至三个工作日内进行审核和修复。',
                'color': '#173177'
            }

        }
        self.notification_to_wxuser(template_id, data, url)

class WeixinKey(models.Model):

    origin_id = models.CharField(max_length = 15, default = '')
    desc = models.CharField(max_length = 10, default = '')
    appid = models.CharField(max_length = 128)
    appsecret = models.CharField(max_length = 128)
    menu = models.TextField(null = True, blank = True)

    create_time = models.DateTimeField(verbose_name=u"创建时间",auto_now_add=True,null=True,editable=True,)
    last_modified_time = models.DateTimeField(editable=True,verbose_name=u"最后修改时间",auto_now=True,null=True)
   
    @property
    def token(self):
        token = cache.get("weixintoken_%s" % str(self.appid))
        if token is not None:
            return token

        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
        data = urllib2.urlopen(url % (self.appid, self.appsecret)).read()
        data = json.loads(data)
        cache.set("weixintoken_%s" % str(self.appid), data["access_token"], 1800)
        return data["access_token"]
