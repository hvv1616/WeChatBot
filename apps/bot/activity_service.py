import requests
from os import times
import time;
from .models import *
from django.db.models import F, Q
from decimal import Decimal
from django.conf import settings
from django.core.cache import caches
from django.db import connection
import json
import threading
from django.core.paginator import Paginator,Page #导入模块

class ActivityService():
    def __init__(self,message):
        self.message=message
        pass
    def fmLoginGetCode(self,mobile):
        '''
        获取发米家验证码
        '''
        url = "https://fmapp.chinafamilymart.com.cn/api/app/member/verifyCode"
        payload="{\"distinctId\":\"\",\"mobile\":\""+mobile+"\",\"firstSend\":true,\"newVersion\":true}"
        headers = {
        'Host': 'fmapp.chinafamilymart.com.cn',
        'Connection': 'keep-alive',
        'Origin': 'https://fmapp-activity.chinafamilymart.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 wxwork/3.1.1 (MicroMessenger/6.2) WindowsWechat',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN',
        'Referer': 'https://fmapp-activity.chinafamilymart.com.cn/login?query=%%257B%%2522response_type%%2522%%253A%%2522token%%2522%%252C%%2522client_id%%2522%%253A%%25225A7CF52A75C1CBFC%%2522%%252C%%2522redirect_uri%%2522%%253A%%2522https%%253A%%252F%%252Fmall-oapi.chinafamilymart.com.cn%%252Fapp%%252Fapi%%252Fv1.0%%252Fmember%%252Flogin%%252Fcallback%%2522%%252C%%2522status%%2522%%253A%%2522status%%2522%%252C%%2522udf1%%2522%%253A%%2522eyJjaGFubmVsIjoiMCIsImZvcndhcmRfdXJsIjoiYUhSMGNITTZMeTl0WVd4c0xXZzFMbU5vYVc1aFptRnRhV3g1YldGeWRDNWpiMjB1WTI0dmNHRm5aWE5CTDJ4dloybHVMMnh2WjJsdVAyaHBjMVZ5YkQwdmNHRm5aWE12YzJodmNIQnBibWREWVhJdmFXNWtaWGc9In0%%253D%%2522%%257D',
        'Accept-Encoding': 'gzip, deflate'
        }
        #response ={"text":"{\"code\":\"200\",\"message\":\"\",\"data\":null}"}
        response = requests.request("POST", url, headers=headers, data=payload)
        body=response.text
        resJObj=json.loads(body)
        print(body,resJObj)
        '''
        {"code":"200","message":"","data":null}
        '''
        if resJObj.get('code')=="200":
            return True
        else :
            return False

    def fmLogin(self,mobile,verifyCode):
        '''
        获取登录信息
        '''
        message=self.message
        url = "https://fmapp.chinafamilymart.com.cn/api/h5/login"
        payload="{\"mobile\":\""+mobile+"\",\"verifyCode\":\""+verifyCode+"\",\"grantTypeCd\":\"1\",\"newVersion\":true,\"openId\":\"\",\"unionId\":\"\",\"openChannelCd\":1}"
        headers = {
        'Host': 'fmapp.chinafamilymart.com.cn',
        'Connection': 'keep-alive',
        'loginChannel': 'yunchao',
        'Origin': 'https://fmapp-activity.chinafamilymart.com.cn',
        'blackBox': 'eyJ2IjoiQ3FlZ2hDMnhNQU9zQ1NRRlhsODR1djMwVkdwYW9kS3p3TUhRNHR5ZXlZbk9BT2NMdHJ3QmVpMDM1WWhyNFJ5ViIsIm9zIjoid2ViIiwiaXQiOjE3MywidCI6InpTVkE0UGpzZGFaWVp1ckRTalpKOUlzb2YvTHNPR1c5SG9QRURFOVBDVnpFNlZTUHM3NXhqd2hlZ0o2SFY5ajdTTTBDQjFiRytlcVpqSFk2WWQ1UHlRPT0ifQ==',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 wxwork/3.1.1 (MicroMessenger/6.2) WindowsWechat',
        'os': 'h5',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN',
        'Referer': 'https://fmapp-activity.chinafamilymart.com.cn/login?query=%%257B%%2522response_type%%2522%%253A%%2522token%%2522%%252C%%2522client_id%%2522%%253A%%25225A7CF52A75C1CBFC%%2522%%252C%%2522redirect_uri%%2522%%253A%%2522https%%253A%%252F%%252Fmall-oapi.chinafamilymart.com.cn%%252Fapp%%252Fapi%%252Fv1.0%%252Fmember%%252Flogin%%252Fcallback%%2522%%252C%%2522status%%2522%%253A%%2522status%%2522%%252C%%2522udf1%%2522%%253A%%2522eyJjaGFubmVsIjoiMCIsImZvcndhcmRfdXJsIjoiYUhSMGNITTZMeTl0WVd4c0xXZzFMbU5vYVc1aFptRnRhV3g1YldGeWRDNWpiMjB1WTI0dmNHRm5aWE5CTDJ4dloybHVMMnh2WjJsdVAyaHBjMVZ5YkQwdmNHRm5aWE12YzJodmNIQnBibWREWVhJdmFXNWtaWGc9In0%%253D%%2522%%257D',
        'Accept-Encoding': 'gzip, deflate'
        }
        #response ={"text":"{\"code\":\"200\",\"message\":\"\",\"data\":{\"token\":\"eyJhbGciOiJIUzUxMiIsInppcCI6IkRFRiJ9.eNo0jU2KAjEQha8ite5AkqpU2txgNrNwnU0lnWZaFBqjMIx4AsFTuPFgMteY-DPwFvW-V493hPV-ggCjlVQ0LlWfdVYk3qmeRBTppDmXMWdi6KAeUns-RjjUsvuUbYkQIvxezov79dYUoXtlH8MzYaKBl2g5s6B12nnvXE8JrUdGJ41qbygROYMDDs--zPO73i6Vpp8Ip7Y91dq23-jhZQ_BsEHjGcl0UL5nCGS1-wdTXZVxV-oXhFE2tZz-AAAA__8.VH_5thEBNiGp4wjF-J1VS3h7bMpzI-hY_Y-_tfVKoIkmu8na3cPYaqsZ1z9JrL8nmRTMJHettX9F7wl7io3g3w\",\"phoneNumber\":null,\"memberCode\":\"644d69326c6a32505775584b3273635a6a30714b44513d3d\",\"bindId\":null,\"lastName\":\"王\",\"realName\":\"王 天天\",\"genderCd\":1,\"birthday\":\"1980-11-29 00:00:00\",\"picUrl\":\"https://fmapp-cos.chinafamilymart.com.cn/image/20210113/1610535732927/IMG_CROP_20210113_19020991.jpeg\",\"nickName\":\"fm_6597\",\"firstLoginFlag\":false,\"perfectInfoFlag\":false,\"open3rd\":null,\"zxMemberFlag\":false,\"activityId\":\"163\"}}"}
        response = requests.request("POST", url, headers=headers, data=payload)
        body=response.text
        '''
        {"code":"200","message":"","data":{"token":"eyJhbGciOiJIUzUxMiIsInppcCI6IkRFRiJ9.eNo0jU2KAjEQha8ite5AkqpU2txgNrNwnU0lnWZaFBqjMIx4AsFTuPFgMteY-DPwFvW-V493hPV-ggCjlVQ0LlWfdVYk3qmeRBTppDmXMWdi6KAeUns-RjjUsvuUbYkQIvxezov79dYUoXtlH8MzYaKBl2g5s6B12nnvXE8JrUdGJ41qbygROYMDDs--zPO73i6Vpp8Ip7Y91dq23-jhZQ_BsEHjGcl0UL5nCGS1-wdTXZVxV-oXhFE2tZz-AAAA__8.VH_5thEBNiGp4wjF-J1VS3h7bMpzI-hY_Y-_tfVKoIkmu8na3cPYaqsZ1z9JrL8nmRTMJHettX9F7wl7io3g3w","phoneNumber":null,"memberCode":"644d69326c6a32505775584b3273635a6a30714b44513d3d","bindId":null,"lastName":"王","realName":"王 天天","genderCd":1,"birthday":"1980-11-29 00:00:00","picUrl":"https://fmapp-cos.chinafamilymart.com.cn/image/20210113/1610535732927/IMG_CROP_20210113_19020991.jpeg","nickName":"fm_6597","firstLoginFlag":false,"perfectInfoFlag":false,"open3rd":null,"zxMemberFlag":false,"activityId":"163"}}
        '''
        resJObj=json.loads(body)
        print(body,resJObj)
        bot_wxid = message.get('user', 'bot_wxid')
        entity = BotChatActivity.objects.filter(
                from_member_wxid=message.get('data', {}).get('from_member_wxid', '')).filter(login_username=mobile).filter(bot_wxid=bot_wxid)
        if resJObj.get('data') is None:
            resJObj['data']={'token':''}
        if not entity.exists():
            bot_activity_entity=BotChatActivity(
                bot_wxid = bot_wxid,
                activity_type='发米家',
                from_member_wxid = message.get('data', {}).get('from_member_wxid', ''),
                from_member_nickname = message.get('data', {}).get('from_nickname',''),
                login_req=payload,
                login_res= body,
                token = resJObj.get('data',{"token":""}).get('token',''),
                is_invalid = '否是',
                update_time = message.get('data', {"time":""}).get('time', ''),
                create_time = message.get('data', {"time":""}).get('time', ''),
                desc ='发米家登录，目前登录后获取token自动签到！',
                login_username=mobile,
                from_chatroom_wxid=message.get('data', {}).get('from_chatroom_wxid', ''),
                from_chatroom_nickname=message.get('data', {}).get('from_chatroom_nickname', ''),
            )
            if resJObj.get('code')=="200":
                bot_activity_entity.is_invalid='否'
            bot_activity_entity.save()
        else:
            if resJObj.get('code')=="200":
                entity.update(is_invalid='否',update_time = message.get('data', {"time":""}).get('time', ''),login_req=payload,login_res= body,token = resJObj.get('data',{"token":""}).get('token'),)
            else:
                entity.update(is_invalid='是',update_time = message.get('data', {}).get('time', ''),login_req=payload,login_res= body,token = resJObj.get('data',{"token":""}).get('token'),)
            pass
        if resJObj.get('code')=="200":
            self.sign(resJObj.get('data',{"token":""}).get('token'))
            return True
        else :
            return False

    def sign(self,token):
        url = "https://fmapp.chinafamilymart.com.cn/api/app/market/member/signin/sign"
        payload={}
        headers = {
        'fmVersion': '2.0.2',
        'loginChannel': 'app',

        'Content-Type': 'application/json',
        'channel': '333',
        'token': ''+token,
        'deviceId': 'b42aee0fa7d44fc44d59749da550f75a',
        'Content-Length': '0',
        'Host': 'fmapp.chinafamilymart.com.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.10.0'
        }

        response = requests.request("POST", url, headers=headers, data=payload)        
        print(response.text)
        return response.text
    def signAll(self):
        entitys = BotChatActivity.objects.filter(is_invalid='否')
        for entity in entitys:
            res=self.sign(entity.token)
            resJObj=json.loads(res)
            entity.sign_result=res
            entity.sign_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if resJObj.get("code","")=="102003" or resJObj.get("code","")==102003:
                entity.is_invalid='是'
            entity.save()
        return entitys.values()
        '''
        {"code":"3004000","message":"今日已签到","data":null}
        {"code":102003,"message":"您的账号已在其它设备上登录，请重新登录","data":null}
        {"code":102002,"message":"连接超时","data":null}
        '''