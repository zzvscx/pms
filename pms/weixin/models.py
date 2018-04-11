#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from useraccount.models import User

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
