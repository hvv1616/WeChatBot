from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
import json
#from .objtest import config,getNum
# from ..bot.bot_start import main,admin_wx
#from ..bot.objtest import config,getNum
num = 0
#wx_inst= main()

# def sendMsg(request):
#     msg=request.GET.get('msg') 
#     global num
#     global config
#     config["a"] +=config["a"]
#     num += 1
#     global wx_inst
#     wx_inst.send_text(admin_wx,msg)
#     return HttpResponse(str(num)+"msg："+msg+json.dumps(config))

# def hello(request):
#     msg=request.GET.get('msg') 
#     global num
#     global config
#     config["a"] +=config["a"]
#     return HttpResponse(str(num)+"msg："+msg+json.dumps(config))

def sendMsg(request):
    msg=request.GET.get('msg') 
   
    return HttpResponse("sendMsg:"+msg)

def hello(request):
    msg=request.GET.get('msg') 
    return HttpResponse("hello:"+msg)
