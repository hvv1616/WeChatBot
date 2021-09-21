# 缓存配置
from django.forms.models import model_to_dict
import uuid
import os
import sys
import requests
import json
import re
import time
import datetime
import random
import hashlib
import hmac
import base64
import xml
import subprocess
import threading
from django.db.models import F, Q
from .bot_service import BotService
from django.core.cache import cache
# 自定义的JWT配置 公共插件
from utils.utils import VisitThrottle, getDistance, NormalObj

from .models import *

from functools import reduce
from urllib.parse import unquote_plus
from decimal import Decimal
from django.conf import settings
from django.core.cache import caches
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import threading
from .models import *
from django.db.models import F, Q
from .get_images import start as get_images_start,download_load
#from .bot_start import main as bot_start_main
from django.http import HttpResponse,response
from .handle_msg import handle_all_message
from .util import Email,getDayImg
from .activity_service import ActivityService
from .WechatPCAPI import WechatPCAPI
from os import path
wx_inst = None
num = 1
# 测试


def test(request):
    activityService=ActivityService({'user': 'wxid_kkp102awseir22', 'type': 'msg::chatroom', 'data': {'data_type': '1', 'send_or_recv': '1+[Demo]', 'from_chatroom_wxid': '19162403962@chatroom', 'from_member_wxid': None, 'time': '2021-3-4 23:20:59', 'msg': '13125110897登录成功！请验证每日活动签到是否成功！如失效请重新操作登录！', 'from_chatroom_nickname': '测试群'}})
    activityService.signAll()
    # default_bot_wxid=BotService.get_config_val("bot_wxid")
    # bs = BotService(bot_wxid=default_bot_wxid)
    # print('bot_wxid',default_bot_wxid)
    
    # #bs.init_bot_data()
    # #bs.addAdminWX("wxid_dg5xnz4s39ea21")
    # # get_images_start()
    # #ls = BotConfig.objects.values()
    # # bs.arrayConfigAdd("group_receive_list","wxid_kkp102awseir22")
    # # bs.arrayConfigDel("group_receive_list","wxid_kkp102awseir22")
    # #print(ls, type(ls))
    # #wx_inst.update_frinds()
    # global num
    # res=bs.getChatroomMsg("17648533871@chatroom",num)
    # num += 1
    # print(res)
    return HttpResponse('res')
def getTimeImg(request):
    d1 = datetime.datetime.now()  # 第一个日期
    d2 = datetime.datetime(2021,5,15)   # 第二个日期
    interval = str(d2 - d1)[0:2]
    interval=interval.replace(" ","")
    filename=os.path.abspath(getDayImg(interval))
    image_data = open(filename,"rb").read()
    return HttpResponse(image_data,content_type="image/png")
def signAll(request):
    activityService=ActivityService({'user': 'wxid_kkp102awseir22', 'type': 'msg::chatroom', 'data': {'data_type': '1', 'send_or_recv': '1+[Demo]', 'from_chatroom_wxid': '19162403962@chatroom', 'from_member_wxid': None, 'time': '2021-3-4 23:20:59', 'msg': '13125110897登录成功！请验证每日活动签到是否成功！如失效请重新操作登录！', 'from_chatroom_nickname': '测试群'}})
    
    return HttpResponse(activityService.signAll())
    
def verify_wx(request):
    signature = request.GET.get("signature")  # 先获取加密签名
    #timestamp = data.timestamp  # 获取时间戳
    nonce = request.GET.get("nonece")  # 获取随机数
    echostr = request.GET.get("echostr") # 获取随机字符串
    print('wx公众号验证=》',signature,nonce,echostr)
    #不验证签名，直接返回echostr，表示公众号服务器验证成功
    return HttpResponse(echostr)
# 获取数据库所有群聊信息
def get_chatroom_list(request):
    if request.method == "POST":
        return HttpResponse("POST")
    else:
        print(request.GET)
        bot_wxid=request.GET.get('bot_wxid')
        kwargs ={}
        if bot_wxid:
            kwargs["bot_wxid"]=bot_wxid
        data=list(BotChatroom.objects.filter(**kwargs).values())    
        return response.JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii': False})
 
# 发送触发bot命令的文本信息
def send_trigger_text(request):
    if request.method == "POST":
        '''
        body json类型
        {"type":"chatroom","bot_wxid":"wxid_kkp102awseir22","to_wxid":"","trigger_msg":""}
        '''
        param=json.loads(request.body.decode())
        bot_wxid=BotService.get_config_val("bot_wxid")
        msg_obj={}
        if param["bot_wxid"]:
            bot_wxid=param["bot_wxid"]
        if param["type"] in "chatroom":#群消息
            msg_obj=chatroom_msg_temp={"user":bot_wxid,"type":"msg::chatroom","data":{"data_type":"1","send_or_recv":"0+[收到]","from_chatroom_wxid":param["to_wxid"],"from_member_wxid":"wxid_dg5xnz4s39ea21","time":"2021-01-17 00:52:14","msg":param["trigger_msg"],"from_chatroom_nickname":"测试2群"}}
        if param["type"] in "signal":#单聊消息
            msg_obj=signal_msg_temp={"user":bot_wxid,"type":"msg::single","data":{"data_type":"1","send_or_recv":"0+[收到]","from_wxid":param["to_wxid"],"time":"2021-01-17 14:10:42","msg":param["trigger_msg"],"from_nickname":"一天"}}
        data={"message": "发送成功", "errorCode": 0, "data":param }
        handle_all_message(wx_inst=wx_inst, message=msg_obj)
        return response.JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii': False}) 
    return HttpResponse('请使用POST请求')
def send_text(request):
    '''
     body json类型
     {"bot_wxid":"wxid_kkp102awseir22","to_user":"","msg":""}
    '''
    param=json.loads(request.body.decode())
    wx_inst.send_text(param["to_user"], param["msg"])    
    return response.JsonResponse({"message": "文本消息发送成功", "errorCode": 0, "data":param },safe=False,json_dumps_params={'ensure_ascii': False}) 

# 发送卡片信息
def send_link_card(request):
    '''
     body json类型
     {"bot_wxid":"wxid_kkp102awseir22","to_user":"","title":"","desc":"","target_url":"","img_url":""}
    '''
    param=json.loads(request.body.decode())
    wx_inst.send_link_card(param["to_user"], param["title"], param["desc"], param["target_url"], param["img_url"])    
    return response.JsonResponse({"message": "card发送成功！", "errorCode": 0, "data":param },safe=False,json_dumps_params={'ensure_ascii': False}) 
# 发送图片

def send_img(request):
    '''
     body json类型
     {"bot_wxid":"wxid_kkp102awseir22","to_user":"","img_url":""}
    '''
    param=json.loads(request.body.decode())
    fileName=re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",param["img_url"])
    if param["img_url"].split('/')[-1].count(".")>0:
        fileName=fileName+os.path.splitext(param["img_url"])[-1]
    else:
        fileName=fileName+".jpg"
    if os.path.exists(os.path.join("./images/send_img", fileName)):
        os.remove(os.path.join("./images/send_img", fileName))
    filePath=os.path.abspath(download_load(param["img_url"],"./images/send_img",fileName))
    wx_inst.send_img(param["to_user"], filePath)
    return response.JsonResponse({"message": "img发送成功", "errorCode": 0, "data":param },safe=False,json_dumps_params={'ensure_ascii': False}) 
def send_file(request):
    '''
     body json类型
     {"bot_wxid":"wxid_kkp102awseir22","to_user":"","file_url":"","file_name":""}
    '''
    param=json.loads(request.body.decode())
    fileName=param["file_name"]
    filePath=os.path.abspath(download_load(param["file_url"],"./images/send_file",fileName))
    print('send_file',filePath)
    wx_inst.send_file(param["to_user"], filePath)
    return response.JsonResponse({"message": "文件发送成功", "errorCode": 0, "data":param },safe=False,json_dumps_params={'ensure_ascii': False}) 
# 监听所有微信消息


def onmessage(request):
    if request.method == "POST":
        msg_obj = json.loads(request.body)
        print('接受post消息：',msg_obj)
        try:
            #handle_all_message(wx_inst=wx_inst, message=msg_obj)
            onMsg(msg_obj)
            return HttpResponse(request.body)
        except Exception as e:
            print('处理错误！开始重启bot...')
            
            email = Email(
            mail_host=BotService.get_config_val("email_host") ,
            mail_user=BotService.get_config_val("email_user") ,
            mail_pwd=BotService.get_config_val("email_pwd") 
            )      
            email.send("微信机器人异常提醒","您的机器人服务出现故障，需要点击以下链接进行重启！<br/><br/> 错误信息："+str(e)+" <br/> <br/> <a href=\""+BotService.get_config_val("bot_api_url")+"/bot/start/\">点击重启</a>",BotService.get_config_val_obj("email_receivers"))
            return HttpResponse(request.body)
    return HttpResponse('get')
def onMsg(msg_obj):
    try:
        print(msg_obj)
        #msg_obj = json.loads(message)
        # time.sleep(0.1)
        handle_all_message(wx_inst=wx_inst, message=msg_obj)
    except Exception as e:
            print('处理错误！开始重启bot...')
            email = Email(
            mail_host=BotService.get_config_val("email_host") ,
            mail_user=BotService.get_config_val("email_user") ,
            mail_pwd=BotService.get_config_val("email_pwd") 
            )      
            email.send("微信机器人异常提醒","您的机器人服务出现故障，需要点击以下链接进行重启！<br/><br/> 错误信息："+str(e)+" <br/> <br/> <a href=\""+BotService.get_config_val("bot_api_url")+"/bot/start/\">点击重启</a>",BotService.get_config_val_obj("email_receivers"))
def bot_start_main():
    wx_inst = WechatPCAPI(on_message=onMsg)
    wx_inst.start_wechat(block=True)
    return wx_inst
# 启动bot
def start(request):
    try:
        print(BotCommand.bot_wxid)
        # get_images_start()
        global wx_inst
        wx_inst = bot_start_main()
        #wx_inst.update_frinds()
        m = PyMouse()
        m.move(957, 600)
        time.sleep(2)#等待2s
        m.click(957, 600)
        k = PyKeyboard()
        # k.press_key(k.windows_l_key) #按住win键
        # k.tap_key('D')#点击D
        # print("触发按钮--->win+D显示桌面")
        # k.release_key(k.windows_l_key)#松开win键
        return HttpResponse(json.dumps({"message": "启动成功", "errorCode": 0, "data": ""}, ensure_ascii=False))
    except Exception as e:
        print('发生错误：', e)
        return HttpResponse(json.dumps({"message": "出现了无法预料的错误：", "errorCode": 0, "data": ""}, ensure_ascii=False))
# 启动微信时自动点击登录

def downloadVideo(request):
    if request.method == "POST":
        return HttpResponse("POST")
    else:
        print(request.GET)
        url=request.GET.get('url')
        response=requests.get("http://127.0.0.1:5000/extract/?url="+url)
        resObj=response.json()
        print(resObj,resObj.get("code"))
        if(resObj.get("code")==200):
            videoUrl=resObj.get("data",{}).get("videos",[])[0]
            return HttpResponse(videoUrl) 
        else:
            return HttpResponse("未找到视频")  

def mouse(request):
    print('准备点击登录.。。')
    time.sleep(2000)
    print('开始点击登录。。。')
    m = PyMouse()
    m.move(957, 600)
    time.sleep(1)
    print('点击登录')
    m.click(957, 600)
    return HttpResponse("ok")
def bank_send_msg1(request,key,body):
    for to_user in key.split(","):
        msg=body
        msg=msg.encode('gbk', 'ignore').decode('gbk', 'ignore').encode("UTF-8").decode("UTF-8")
        wx_inst.send_text(to_user, msg)    
    return HttpResponse(json.dumps({"message": "推送到群组："+key+"，成功！","code":200, "errorCode": 0, "data": ""}, ensure_ascii=False))       
def bank_send_msg2(request,key,title,body):
    print('key======>',key,'title======>',title,'body======>',body)
    for to_user in key.split(","):  
        msg=title+"\r\n"+body 
        msg=str(msg).encode('gbk', 'ignore').decode('gbk', 'ignore').encode("UTF-8").decode("UTF-8")
        print("msg=====>:",msg)
        wx_inst.send_text(to_user, msg)    
    return HttpResponse(json.dumps({"message": "推送到群组："+key+"，成功！","code":200, "errorCode": 0, "data": ""}, ensure_ascii=False))    

