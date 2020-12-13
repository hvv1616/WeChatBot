# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 23:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    :
# @Software: PyCharm

from WechatPCAPI import WechatPCAPI
import time
import logging
from datetime import date
from queue import Queue
import threading

logging.basicConfig(level=logging.INFO)


def on_message(message):
    print("message->:",message)
    # {
    # 'user': 'wxid_kkp102awseir22', 
    # 'type': 'msg::chatroom', 
    # 'data': {
    #         'data_type': '1', 
    #         'send_or_recv': '0+[收到]', 
    #         'from_chatroom_wxid': '19162403962@chatroom', 
    #         'from_member_wxid': 'wxid_dg5xnz4s39ea21',
    #         'time': '2020-12-11 13:26:27',
    #         'msg': '测试消息test111', 
    #         'from_chatroom_nickname': '测试群'
    #         }
    # }

    msg_obj=message
    print("obj->:",msg_obj)
    if msg_obj["type"]=="msg::chatroom":
        print("tset0")
        if(msg_obj["data"]["from_chatroom_nickname"].index("测试群")>-1):
            print("tset1")
            if(msg_obj["data"]["msg"].index("测试")>-1):
                print("tset2")
                print(wx_obj)
                wx_obj.send_text(to_user=msg_obj["data"]["from_chatroom_wxid"], msg='你真帅！')


def main():
    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    wx_inst.start_wechat(block=True)
    wx_obj=wx_inst
    print(wx_obj)
    while not wx_inst.get_myself():
        time.sleep(5)
    wx_obj=wx_inst
    
    
    # # from_group_name="" # 来自哪个组
    # # if "from_chatroom_nickname" in dict: 
    # #     from_group_name=msg_obj.from_chatroom_nickname; # 来自哪个组
    # # from_group_id="" # 来自哪个组id
    # # if "from_chatroom_wxid" in dict: 
    # #     from_group_name=msg_obj.from_chatroom_wxid; # 来自哪个组id
    # from_group_name=msg_obj.data.from_chatroom_nickname

    # msg=wx_inst.get_myself().data.msg # 消息
    # from_user=wx_inst.get_myself().data.user; # 来自哪个用户
    # now = datetime.now()
    # now_str=str(new)
   

    # time.sleep(10)
    # # wx_inst.send_text(to_user='filehelper', msg='777888999')
    # # wx_inst.send_link_card(
    # #     to_user='filehelper',
    # #     title='博客',
    # #     desc='我的博客，红领巾技术分享网站',
    # #     target_url='http://www.honglingjin.online/',
    # #     img_url='http://honglingjin.online/wp-content/uploads/2019/07/0-1562117907.jpeg'
    # # )
    # # wx_inst.send_img(to_user='filehelper', img_abspath=r'C:\Users\Leon\Pictures\1.jpg')
    # #wx_inst.send_file(to_user='filehelper', file_abspath=r'C:\Users\Leon\Desktop\1.txt')
    # #wx_inst.send_gif(to_user='filehelper', gif_abspath=r'C:\Users\Leon\Desktop\08.gif')
    # #wx_inst.send_card(to_user='filehelper', wx_id='gh_6ced1cafca19')
    # print("打印:::：")
    # print("打印：",from_group_name,now_str,from_user)
    # if from_group_name=="测试群" :
    #     if now_str.count('18:00')>=1 or now_str.count('12:27') :
    #         wx_inst.send_text(to_user=from_group_name, msg='测试111')
    # # wx_inst.update_frinds()
    #     if msg=="测试" or msg == "test" :
    #          wx_inst.send_text(to_user=from_group_name, msg='您发送了一条测试消息，嘻嘻嘻！')

if __name__ == '__main__':
    main()
