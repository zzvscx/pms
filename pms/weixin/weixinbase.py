#coding:utf-8



import json
import xml.etree.ElementTree as ET  
import time
import hashlib  

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt  
from django.utils.encoding import smart_unicode  
from django.db import transaction

from .models import  WeixinUser

TOKEN = "changan"


class MsgType(object):
    
    def __init__(self, funcflag=False):
        self.funcflag = funcflag
    
    def get_ret_xml(self, msg):
        container = '''
<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
%s
    <FuncFlag>%s</FuncFlag>
</xml>'''
        
        content = self.get_xml()
        full_xml = container %(msg['FromUserName'], msg['ToUserName'], str(int(time.time())), content, '1' if self.funcflag else '0')
        return full_xml
    
    def get_xml(self):
        return ''


class Text(MsgType):

    xmltempl = '''
    <MsgType><![CDATA[%s]]></MsgType>
    <Content><![CDATA[%s]]></Content>
'''
    
    def __init__(self,text, funcflag=False):
        super(Text, self).__init__(funcflag)
        self.text = text

    def get_xml(self):
        if self.text:
            xmltempl = self.xmltempl % ('text', self.text)
        else:
            xmltempl = None
        return xmltempl


class Music(MsgType):

    xmltempl = '''
 <MsgType><![CDATA[music]]></MsgType>
 <Music>
 <Title><![CDATA[%s]]></Title>
 <Description><![CDATA[%s]]></Description>
 <MusicUrl><![CDATA[%s]]></MusicUrl>
 <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
 </Music>
'''
    def __init__(self, title, desc, musicurl, hqurl, funcflag=False):
        self.title = title
        self.desc = desc
        self.musicurl = musicurl
        self.hqurl = hqurl

    def get_xml(self):
        try:
            return xmltempl %(self.title, self.desc, self.musicurl, self.hqurl)
        except:
            return None

class News(MsgType):
    xmltempl = '''
 <MsgType><![CDATA[news]]></MsgType>
 <ArticleCount>{count}</ArticleCount>
 <Articles>
 {items}
 </Articles>
'''
    item = '''
<item>
<Title><![CDATA[{title}]]></Title> 
<Description><![CDATA[{description}]]></Description>
<PicUrl><![CDATA[{picurl}]]></PicUrl>
<Url><![CDATA[{url}]]></Url>
</item>
'''
    articlelimit = 10
    def __init__(self, items, funcflag=False):
        super(News, self).__init__(funcflag)
        self.items = items

    def get_xml(self):
        
        return self.xmltempl.format(**{
            "count" : len(self.items),
            "items" : "".join([self.item.format(**x) for x in self.items])
            })
        if self.text:
            xmltempl = self.xmltempl % ('text', self.text)
        else:
            xmltempl = None
        return xmltempl
    pass

class Image(MsgType):
    xmltempl = '''
 <MsgType><![CDATA[image]]></MsgType>
 <PicUrl><![CDATA[%s]]></PicUrl>
'''
    def __init__(self, picurl, funcflag=False):
        super(Image, self).__init__(self, funcflag)
        self.picurl = picurl

    def get_xml(self):
        if picurl:
            return xmltempl %(self.picurl)
        else:
            return None

class Link(MsgType):
    xmltempl = '''
<MsgType><![CDATA[link]]></MsgType>
<Title><![CDATA[公众平台官网链接]]></Title>
<Description><![CDATA[公众平台官网链接]]></Description>
<Url><![CDATA[url]]></Url>
'''
    def __init__(self, title, desc, url):
        self.title = title
        self.description = desc
        self.url = url


class Location(MsgType):
    
    xmltempl = '''
<MsgType><![CDATA[location]]></MsgType>
<Location_X>23.134521</Location_X>
<Location_Y>113.358803</Location_Y>
<Scale>20</Scale>
<Label><![CDATA[位置信息]]></Label>
'''
    def __init__(self, loc_x, loc_y, scale, label):
        self.location_x = loc_x
        self.location_y = loc_y
        self.scale = scale
        self.label - label
    pass

class Transfer_Customer_Service(MsgType):

    xmltempl = '''
<xml>
<ToUserName><![CDATA[{touser}]]></ToUserName>
<FromUserName><![CDATA[{fromuser}]]></FromUserName>
<CreateTime>{CreateTime}</CreateTime>
<MsgType><![CDATA[transfer_customer_service]]></MsgType>
</xml>
'''

    def __init__(self, msg):
        self.msg = msg

    def get_ret_xml(self, msg):
        msg = self.msg
        return self.xmltempl.format(**{
            'touser': msg["FromUserName"],
            'fromuser': msg["ToUserName"],
            'CreateTime': int(time.time()),
            })

class WeixinBase(object):

    def __init__(self, request):
        rawStr = smart_unicode(request.raw_post_data)
        #print request.raw_post_data
        #import code;code.interact(local=locals())
        print rawStr
        msg = parseMsgXml(ET.fromstring(rawStr))  
        self.msg_dict = msg
        self.fromuser = self.getfromuser()
    
    def response_msg(self):
        msg_handler = {
            "text": (self.response_text, self.get_text) ,
            "event": (self.process_event, None) ,
            }
        msgtype = self.msg_dict['MsgType']
        handler = msg_handler.get(msgtype, None)
        if handler[1]:
            ret_obj = handler[0](handler[1]())
        else:
            ret_obj = handler[0]()
        return ret_obj.get_ret_xml(self.msg_dict)
        
    def process_event(self):
        event_handler = {
            "subscribe": self.response_subscribe,
            "unsubscribe": self.response_unsubscribe,
            }
        handler = self.msg_dict.get('Event', None)
        if handler:
            return event_handler[handler]()
        else:
            return None
    
    def response_subscribe(self):
        try:
            wobj = wxu.objects.get(weixin_id=self.getfromuser())
            wobj.issubscribe = True
            wobj.subcount += 1
            wobj.save()
        except:
            wobj = wxu(weixin_id=self.getfromuser(), issubscribe=True, subcount=1)
            wobj.save()
    
    def response_unsubscribe(self):
        try:
            wobj = wxu.objects.get(weixin_id=self.getfromuser())
            wobj.issubscribe = False
            wobj.save()
        except:
            wobj = wxu(weixin_id=self.getfromuser(), issubscribe=False, subcount=1)
            wobj.save()

    def response_text(self, text):
        msg = text.text
        replymsg = "我也会说:"+ msg
        return Text(replymsg)

    def response_music(self, music):
        return None

    def getfromuser(self):
        return str(self.msg_dict['FromUserName'].strip())

    def get_text(self):
        return Text(self.msg_dict.get('Content', None))
    
    def get_music(self):
        return None


@csrf_exempt
def handleRequest(request, wxclass=WeixinBase):  
    
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request),content_type="text/plain")
        return response  
    elif request.method == 'POST':

        if checkSignature(request) is None:
            return HttpResponse("None")
        rawStr = smart_unicode(request.body)
        print rawStr
        msg = parseMsgXml(rawStr)  
        handler = Handler.get(msg["MsgType"], defaulthandler)
        if isinstance(handler, dict):
            res = handler.get(msg["Event"], defaulthandler)(msg)
        else:
            res = handler(msg)
        #self.msg_dict = msg
        #self.fromuser = self.getfromuser()
        #wx = wxclass(request)
        #re_msg = wx.response_msg()
        
        response = HttpResponse(res.get_ret_xml(msg),content_type="application/xml")
        
        return response  

    else: 
        return HttpResponse("Not Support") 
 
def checkSignature(request):  
    global TOKEN  
    signature = request.GET.get("signature", None)  
    timestamp = request.GET.get("timestamp", None)  
    nonce = request.GET.get("nonce", None)  
    echoStr = request.GET.get("echostr",True)  
    print signature,timestamp,nonce,echoStr
    token = TOKEN  
    tmpList = [token,timestamp,nonce]  
    tmpList.sort()  
    tmpstr = "%s%s%s" % tuple(tmpList)  
    tmpstr = hashlib.sha1(tmpstr).hexdigest()  
    if tmpstr == signature:  
        return echoStr
    else:  
        return None#"%s,%s,%s,%s" % (signature,timestamp,nonce,echoStr)  
  
def parseMsgXml(msg):  
    rootElem = ET.fromstring(msg)
    msg = {"data": msg}
    if rootElem.tag == 'xml':  
        for child in rootElem:  
            msg[child.tag] = smart_unicode(child.text).strip()  
            print child.tag, msg[child.tag]
    #import code; code.interact(local=locals())
    #print msg
    return msg


def register(msgType, event = None):
    def _inner(func):
        if msgType == "event" and event is None:
            Handler[msgType][func.__name__] = func
        elif event:
            Handler[msgType][event] = func
        else:
            Handler[msgType] = func
        return func
    return _inner

def defaulthandlerDYH(msg):

    def subscribe(msg):
        try:
            wxuser = WeixinUser.objects.get(openid = msg["FromUserName"])
        except WeixinUser.DoesNotExist:
            wxuser = WeixinUser()
        wxuser.openid = msg["FromUserName"]
        wxuser.subscribe = 1
        wxuser.save()
        return Text(('欢迎关注长安大学学生成绩管理系统服务号'))

# @csrf_exempt
# def handleRequestDYH(request, wxclass=WeixinBase):  
    
#     if request.method == 'GET':
#         response = HttpResponse(checkSignature(request),content_type="text/plain")
#         return response  
#     elif request.method == 'POST':

#         #if checkSignature(request) is None:
#             #return HttpResponse("None")
#         rawStr = smart_unicode(request.body)
#         print rawStr
#         msg = parseMsgXml(rawStr)  
#         #handler = Handler.get(msg["MsgType"], defaulthandlerDYH)
#         handler = defaulthandlerDYH
#         #if isinstance(handler, dict):
#             #res = handler.get(msg["Event"], defaulthandler)(msg)
#         #else:
#         res = handler(msg)
#         #self.msg_dict = msg
#         #self.fromuser = self.getfromuser()
#         #wx = wxclass(request)
#         #re_msg = wx.response_msg()
        
#         response = HttpResponse(res.get_ret_xml(msg),content_type="application/xml")
        
#         return response  

#     else: 
#         return HttpResponse("Not Support") 
