import base64, json, re, datetime, time
from calendar import timegm
from django.core.cache import cache
import hashlib
import random
import datetime
import time
import math
import requests


# 频率组件

VISIT_RECORD = {}
class VisitThrottle():
    def __init__(self):
        self.history = None

    def allow_request(self,request,view):
        remote_addr = request.META.get('HTTP_X_REAL_IP')
        # print('请求的IP：',remote_addr)
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime,]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history
        while history and history[-1] < ctime - 60:
            history.pop()
        if len(history) < 100:  # 限制的频数 设置同一IP该接口一分钟内只能被访问100次
            history.insert(0, ctime)
            return True
        else:
            return False

    def wait(self):
        ctime = time.time()
        return 60 - (ctime-self.history[-1])



# 公共类
class NormalObj(object):

    def create_password(self, password):
        # 生成加密密码 参数：password
        h = hashlib.sha256()
        h.update(bytes(password, encoding='utf-8'))
        h_result = h.hexdigest()
        return h_result

    def create_code(self):
        # 生成随机验证码
        base_str = '0123456789qwerrtyuioplkjhgfdsazxcvbnm'
        return ''.join(random.sample(base_str, 6))

    def create_order(self, order_type):
        # 生成订单编号 参数订单类型：order_type
        now_date_time_str = str(
            datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
        base_str = '01234567890123456789'
        random_num = ''.join(random.sample(base_str, 6))
        random_num_two = ''.join(random.sample(base_str, 5))
        order_num = now_date_time_str + str(order_type) + random_num + random_num_two
        return order_num


def getDistance(lat1, lng1, lat2, lng2):
    # 计算两经纬度之间的距离 返回距离单位为公里
    radLat1 = (lat1 * math.pi / 180.0)
    radLat2 = (lat2 * math.pi / 180.0)
    a = radLat1 - radLat2
    b = (lng1 * math.pi / 180.0) - (lng2 * math.pi / 180.0)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
    s = s * 6378.137
    return s