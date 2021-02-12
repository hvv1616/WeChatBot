import re
import requests
import urllib.request
import random
from requests.models import Response
from bs4 import BeautifulSoup
import os
import time
from pyquery import PyQuery as pq
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'cookie': 'UM_distinctid=176e68552f72a0-0143a6ad5c850e-c791039-1fa400-176e68552f8434; CNZZDATA1278970723=1364019149-1610181340-%7C1610181340',
    'pragma': 'no-cache',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}


def download_load(url, filepath, name):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = os.path.join(filepath, name)
    if os.path.exists(filename):
        return filename
    print(filename, '开始下载')
    try:
        with open(filename, 'wb')as fp:
            fp.write(requests.get(url).content)
            print(filename+"下载成功")
            fp.close()
    except Exception as e:
        print(filename+'下载失败！！！！！！！！！！！', e)
    return filename
    pass

def getPage(url):
    print('请求页面==>', url)
    return requests.get(url=url, headers=headers)


hrefs = []


def getDetailPage(href, filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    if hrefs.count(href) > 0:
        return
    hrefs.append(href)
    res = getPage(href)
    html_string = res.content.decode("utf-8")
    doc = pq(html_string)
    imgs = doc(".content>img")
    for item in imgs:
        img = pq(item)
        src = img.attr("src")
        download_load(src, filepath, img.attr("alt").replace(
            "/", "").replace("\\", "").replace(".", "")+".jpg")
        nextHref = doc("#pages .a1:eq(1)").attr("href")
        getDetailPage(nextHref, filepath=filepath)
        pass


def start():
    url = "https://www.tujigu.com/"
    response = getPage(url)
    doc = pq(response.content.decode("utf-8"))
    a_list = doc('.hezi:eq(1)').find('.biaoti>a')
    for i in doc('.hezi:eq(1)').find('.biaoti>a'):
        item = pq(i)
        getDetailPage(item.attr("href"), "./images/每日推荐/" +
                      time.strftime("%Y-%m-%d", time.localtime()) + "/"+item.text())
    
    # cate_list = [
    #     {"性感": "https://www.tujigu.com/s/35/"},
    #     {"性感少女": "https://www.tujigu.com/s/186/"},
    #     {"性感": "https://www.tujigu.com/s/35/"},
    #     {"性感": "https://www.tujigu.com/s/35/"},
    #     {"性感": "https://www.tujigu.com/s/35/"},
    #     {"性感": "https://www.tujigu.com/s/35/"},
    # ]
def start_all():
    download_cate("https://www.tujigu.com/s/186/", "性感少女")
    download_cate("https://www.tujigu.com/s/149/", "萌女")
    download_cate("https://www.tujigu.com/s/47/", "极品")
    download_cate("https://www.tujigu.com/s/49/", "比基尼")
    download_cate("https://www.tujigu.com/s/59/", "女神")
    download_cate("https://www.tujigu.com/s/74/", "外拍")
    download_cate("https://www.tujigu.com/s/16/", "蕾丝")
def download_cate(href, cate_name):
    response = getPage(href)
    doc = pq(response.content.decode("utf-8"))
    a_list = doc('.hezi:eq(0)').find('.biaoti>a')
    for i in doc('.hezi:eq(0)').find('.biaoti>a'):
        item=pq(i)
        getDetailPage(item.attr("href"),"./images/"+cate_name+"/"+item.text())
        pass
    hrefs.append(href)
    nextHref = "https://www.tujigu.com"+doc('.next').attr("href")
    if hrefs.count(nextHref) > 0:
        return
    print('nextHref', nextHref)
    download_cate(nextHref, cate_name)


#start()
# download_cate("https://www.tujigu.com/s/186/", "性感少女")
# download_cate("https://www.tujigu.com/s/35/", "性感")

import random

def listdir(path, list_name):  # 传入存储的list
    print(path,os.listdir(path))
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)
def dirStart(isLoad):
    #list=['./images\每日推荐\\-01-11\Hikumi Hisamatsu 久松郁実 [YS-Web] Vol.804 写真集\Hikumi Hisamatsu 久松郁実 [YS-Web] Vol804 写真集21.jpg ']
    list=[]
    if isLoad or len(list)<=0:
        listdir("./images/",list)
    print(os.path.abspath(list[random.randint(0,len(list)-1)]))
    
    pass
# dirStart(False)


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)
    
filePathList=[]            
def randomFile(isLoad):
    global filePathList
    if isLoad or len(filePathList)<=0:
        filePathList=[] 
        listdir("./images/",filePathList) 
    filePath=os.path.abspath(filePathList[random.randint(0,len(filePathList)-1)]) 
    print('随机到图片===>',filePath)
    return filePath