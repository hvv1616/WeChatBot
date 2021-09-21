from genericpath import isdir
import re
import requests
import urllib.request
import random
from requests.models import Response
from bs4 import BeautifulSoup
import os
import time
from pyquery import PyQuery as pq, text
import io
import sys
import chardet
import gzip
import threading
import time
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "Hm_lvt_c08bad6ac66a035b30e72722f365229b=1630671219; Hm_lpvt_c08bad6ac66a035b30e72722f365229b=1630677972"
}

abspath = "F:\\alidrive2\\files"


def code_conversion(response):
    '''
    解决requests的编码问题
    :param response: requests库请求过来的响应体
    :return:
    '''
    html = response.content
    htmltxt = ''
    encode_type = chardet.detect(html)['encoding']
    if encode_type == None:
        try:
            htmltxt = gzip.decompress(html).decode('GB2312', 'ignore')
        except Exception as aa:
            print(aa)
            print('使用压缩文件转换编码时出现了问题')
    else:
        try:
            htmltxt = response.content.decode(str(encode_type), 'ignore')
        except Exception as ee:
            print(ee)
            print('编码格式出现了问题，需要转换的编码为', encode_type)
    return htmltxt


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
    try:
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        res = getPage(href)
        html_string = code_conversion(res)
        doc = pq(html_string)
        nextHref = ""

        if href.split('_').__len__() == 2:
            nextHref = href.split(
                '_')[0]+"_"+str(int(href.split('_')[1].replace('.html', ''))+1)+'.html'
            print(int(href.split('_')[1].replace('.html', '')), '===', int(
                pq(doc(".pages a")[0]).text().replace('共', "").replace("页:", "").replace(' ', '')))
            if int(href.split('_')[1].replace('.html', '')) == int(pq(doc(".pages a")[0]).text().replace('共', "").replace("页:", "")):
                nextHref = ""
        else:
            nextHref = href.split('_')[0].replace('.html', '')+'_2.html'

        print(3)
        imgs = doc("#bigpic img")
        if imgs == None or imgs == "":
            return
        for item in imgs:
            img = pq(item)
        src = img.attr("src")
        download_load(src, filepath, doc(".list_con h1").text().replace(
            "/", "").replace("\\", "").replace(".", "")+".jpg")
        if nextHref == "":
            return
        getDetailPage(nextHref, filepath=filepath)
        pass
    except Exception as e:
            print('getDetailPage错误！', href)
            return


def pageList(url, cate):
    # # 清纯美女
    # url = "https://www.tupianzj.com/meinv/xiezhen/list_179_1.html"
    response = getPage(url)
    doc = pq(code_conversion(response))
    a_list = doc('.list_con_box a')
    for i in a_list:
        item = pq(i)
        if item.attr("href") != None and item.attr("href").count('.html') > 0:
            filepath = ""
            global abspath
            filepath = abspath
            filepath = "./images" if filepath == "" else filepath + "/images"
            # abspath = "./images"
            getDetailPage("https://www.tupianzj.com/"+item.attr("href"),
                        filepath+"/美女/"+cate+"/" + "/"+item.find('label').text())
    nextUrl = ''
    for i in doc('.pages a'):
        if pq(i).text() == "下一页":
            nextUrl = "/".join(url.split('/')[0:-1])+"/"+pq(i).attr("href")
    if nextUrl != '':
        pageList(nextUrl, cate)
    else:
        pass


class myThread (threading.Thread):  # 继承父类threading.Thread
    def __init__(self, url, cate):
        threading.Thread.__init__(self)
        self.url = url
        self.cate = cate

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        try:
            pageList(self.url, self.cate)
        except Exception as e:
            print('错误！', self.cate, self.url, e)


def start():
    print(123)
    thread1 = myThread(
        "https://www.tupianzj.com/meinv/xiezhen/list_179_1.html", "清纯美女")
    thread2 = myThread(
        "https://www.tupianzj.com/meinv/xinggan/list_176_1.html", "性感美女")
    thread3 = myThread(
        "https://www.tupianzj.com/meinv/yishu/list_178_9.html", "人体艺术")
    thread4 = myThread(
        "https://www.tupianzj.com/meinv/siwa/list_193_1.html", "丝袜美女")
    thread5 = myThread(
        "https://www.tupianzj.com/meinv/chemo/list_194_1.html", "香车美人")
    # thread6 = myThread("https://www.tupianzj.com/meinv/mm/list_218_1.html", "美女专区")
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    # thread6.start()


def start_all():
    pageList("https://www.tupianzj.com/meinv/xiezhen/list_179_1.html", "清纯美女")
# start()
# def getDetailPage(href, filepath):
#     if not os.path.exists(filepath):
#         os.makedirs(filepath)
#     if hrefs.count(href) > 0:
#         return
#     hrefs.append(href)
#     res = getPage(href)
#     html_string = res.content.decode("utf-8")
#     doc = pq(html_string)
#     imgs = doc(".content>img")
#     for item in imgs:
#         img = pq(item)
#         src = img.attr("src")
#         download_load(src, filepath, img.attr("alt").replace(
#             "/", "").replace("\\", "").replace(".", "")+".jpg")
#         nextHref = doc("#pages .a1:eq(1)").attr("href")
#         getDetailPage(nextHref, filepath=filepath)
#         pass


# def start():
#     url = "https://www.tujigu.com/"
#     response = getPage(url)
#     doc = pq(response.content.decode("utf-8"))
#     a_list = doc('.hezi:eq(1)').find('.biaoti>a')
#     for i in doc('.hezi:eq(1)').find('.biaoti>a'):
#         item = pq(i)
#         getDetailPage(item.attr("href"), "./images/每日推荐/" +
#                       time.strftime("%Y-%m-%d", time.localtime()) + "/"+item.text())

#     # cate_list = [
#     #     {"性感": "https://www.tujigu.com/s/35/"},
#     #     {"性感少女": "https://www.tujigu.com/s/186/"},
#     #     {"性感": "https://www.tujigu.com/s/35/"},
#     #     {"性感": "https://www.tujigu.com/s/35/"},
#     #     {"性感": "https://www.tujigu.com/s/35/"},
#     #     {"性感": "https://www.tujigu.com/s/35/"},
#     # ]
# def start_all():
#     download_cate("https://www.tujigu.com/s/186/", "性感少女")
#     download_cate("https://www.tujigu.com/s/149/", "萌女")
#     download_cate("https://www.tujigu.com/s/47/", "极品")
#     download_cate("https://www.tujigu.com/s/49/", "比基尼")
#     download_cate("https://www.tujigu.com/s/59/", "女神")
#     download_cate("https://www.tujigu.com/s/74/", "外拍")
#     download_cate("https://www.tujigu.com/s/16/", "蕾丝")
# def download_cate(href, cate_name):
#     response = getPage(href)
#     doc = pq(response.content.decode("utf-8"))
#     a_list = doc('.hezi:eq(0)').find('.biaoti>a')
#     for i in doc('.hezi:eq(0)').find('.biaoti>a'):
#         item=pq(i)
#         getDetailPage(item.attr("href"),"./images/"+cate_name+"/"+item.text())
#         pass
#     hrefs.append(href)
#     nextHref = "https://www.tujigu.com"+doc('.next').attr("href")
#     if hrefs.count(nextHref) > 0:
#         return
#     print('nextHref', nextHref)
#     download_cate(nextHref, cate_name)


# start()
# download_cate("https://www.tujigu.com/s/186/", "性感少女")
# download_cate("https://www.tujigu.com/s/35/", "性感")


def listdir(path, list_name):  # 传入存储的list
    print(path, os.listdir(path))
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)


def dirStart(isLoad):
    # list=['./images\每日推荐\\-01-11\Hikumi Hisamatsu 久松郁実 [YS-Web] Vol.804 写真集\Hikumi Hisamatsu 久松郁実 [YS-Web] Vol804 写真集21.jpg ']
    list = []
    if isLoad or len(list) <= 0:
        listdir("./images/", list)
    print(os.path.abspath(list[random.randint(0, len(list)-1)]))

    pass
# dirStart(False)


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            print(file_path)
            list_name.append(file_path)
            # fsize = os.path.getsize(file_path)
            # if fsize<=0:
            #     print('删除损坏文件：',file_path)
            #     os.remove(file_path)


# def randomlistdir(path):  # 传入存储的list
#     for file in os.listdir(path):
#         file_path = os.path.join(path, file)
#         if os.path.isdir(file_path):
#             listdir(file_path, list_name)
#         else:
#             list_name.append(file_path)
#             fsize = os.path.getsize(file_path)
#             if fsize<=0:
#                 print('删除损坏文件：',file_path)
#                 os.remove(file_path)
filePathList = []


def randomFile2(isLoad):
    global filePathList
    if isLoad or len(filePathList) <= 0:
        filePathList = []
        global abspath
        if abspath != "":
            filePath = abspath+"/"
        else:
            abspath = "./images/"
        listdir(abspath, filePathList)

    filePath = os.path.abspath(
        filePathList[random.randint(0, len(filePathList)-1)])
    print('随机到图片===>', filePath)
    return filePath


def randomFile(isLoad):  # 传入存储的list
    global abspath
    if abspath != "":
        filePath = abspath+"/"
    else:
        abspath = "./images/"
    for i in [0,1,2,3,4]:
        result=getRandomFile(abspath)
        if result:
            return result
        else:
            continue
     

def getRandomFile(path):
   files= os.listdir(path)
   #print(files)
   if files:
    file=files[random.randint(0, len(files)-1)]
    file_path = os.path.join(path, file)
    print(file_path)
    if os.path.isdir(file_path):
        return getRandomFile(file_path)
    else:
        return file_path
   else:
    return None
   
#randomFile(True)
