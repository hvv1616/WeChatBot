import re
import requests
import os
import json
from .bot_service import BotService
from .get_images import randomFile, filePathList, start as get_today_image_start, start_all as get_all_image
from .models import *
bot_name = "@天天bot"
admin_wx = "admin_wx"
host = "http://127.0.0.1:8000"


def handle_all_message(wx_inst, message):

    bot_wxid =message.get('user', 'bot_wxid')
    BotService.load_bot_config(bot_wxid=bot_wxid)
    global admin_wx
    admin_wx = BotService.get_config_val("admin_wx")
    if not admin_wx:
        admin_wx = "admin_wx"
    bot = BotService(bot_wxid=bot_wxid)
    bot.saveMsg(message)
    send_or_recv = message.get('data', {}).get(
        'send_or_recv', '')  # 0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复
    if 'msg::single' in message.get('type'):
        handle_single_message(wx_inst, message)

    if 'msg::chatroom' in message.get('type') and send_or_recv[0] == '0':
        handle_group_message(wx_inst, message)


def handle_single_message(wx_inst, message):
    send_or_recv = message.get('data', {}).get(
        'send_or_recv', '')  # 0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复
    from_wxid = message.get('data', {}).get(
        'from_wxid', '')  # 发送消息的用户id
    msg_content = message.get('data', {}).get('msg', '')  # 消息内容
    bot_wxid = message.get('user', 'bot_wxid')
    if send_or_recv[0] == "1":
        print(from_wxid+"发出消息===>", message)
    if send_or_recv[0] == "0":
        bot = BotService(bot_wxid=bot_wxid)
        if msg_content == "我是你爹":
            if bot.addAdminWX(from_wxid):
                wx_inst.send_text(from_wxid, "添加管理员成功！")
            else:
                wx_inst.send_text(from_wxid, "我已经有爹了，添加管理员失败！")
        if msg_content == "初始化爹":
            bot.del_bot_data()
            wx_inst.send_text(from_wxid, "重置机器人配置成功！")


def handle_group_message(wx_inst, message):
    print("处理群组消息===>", message)
    data_type = message.get('data', {}).get('data_type', '')  # 数据类型
    from_chatroom_wxid = message.get('data', {}).get(
        'from_chatroom_wxid', '')  # 来自群组id
    msg_content = message.get('data', {}).get('msg', '')  # 消息内容
    from_wxid = message.get('data', {}).get(
        'from_member_wxid', '')  # 发送消息的用户id
    from_chatroom_nickname = message.get(
        'data', {}).get('from_chatroom_nickname', '')
    bot_wxid = message.get('user', 'bot_wxid')
    botService = BotService(bot_wxid=bot_wxid)
    # ####################################################################################################===>>>管理员操作命令
    if from_wxid == admin_wx and re.match(r'^['+bot_name+']+[\s\?]+管理[员]*命令[\s]*.+', msg_content):
        content_cmd = re.match(r'^['+bot_name+']+[\s\?]+管理[员]*命令[\s]*(.+)',
                               msg_content).group(1).replace("@", "").replace("?", "")
        print('管理员命令==>>', content_cmd)
        b = False
        if content_cmd == "添加群组":
            botService.arrayConfigAdd("group_receive_list", from_chatroom_wxid)
            b = True
        if content_cmd == "删除群组":
            botService.arrayConfigDel("group_receive_list", from_chatroom_wxid)
            b = True
        if content_cmd == "添加vip群组":
            botService.arrayConfigAdd("group_vip_list", from_chatroom_wxid)
            b = True
        if content_cmd == "删除vip群组":
            botService.arrayConfigDel("group_supvip_list", from_chatroom_wxid)
            b = True
        if content_cmd == "添加supvip群组":
            botService.arrayConfigAdd("group_supvip_list", from_chatroom_wxid)
            b = True
        if content_cmd == "删除supvip群组":
            botService.arrayConfigDel("group_vip_list", from_chatroom_wxid)
            b = True
        if content_cmd == "添加test群组":
            botService.arrayConfigAdd("group_test_list", from_chatroom_wxid)
            b = True
        if content_cmd == "删除test群组":
            botService.arrayConfigDel("group_test_list", from_chatroom_wxid)
            b = True
        if content_cmd == "添加黑名单":
            botService.arrayConfigAdd("group_back_list", from_chatroom_wxid)
            b = True
        if content_cmd == "删除黑名单":
            botService.arrayConfigDel("group_back_list", from_chatroom_wxid)
            b = True
        if content_cmd == "重新加载配置":
            botService.reload_bot_config()
            b = True
        if content_cmd == "更新图片":
            randomFile(isLoad=True)
            b = True
        if content_cmd == "爬每日推荐图片":
            get_today_image_start()
            b = True
        if content_cmd == "爬所有图片":
            get_all_image()
            b = True
        if content_cmd == "重启":
            requests.get(host+"/bot/start/")
            b = True
        if b:
            wx_inst.send_text(from_chatroom_wxid, content_cmd+"成功！")
        else:

            wx_inst.send_text("没有这个命令！")
        return
    # #####################################################################################################==>>>拦截黑名单群组
    if (from_chatroom_wxid in BotService.get_config_val_obj("group_back_list")):
        return
    # #####################################################################################################==>>>test测试群组功能
    if data_type[0] == '1' and (from_chatroom_wxid in BotService.get_config_val_obj("group_test_list")):
        # 群舔人
        if re.match(r'^['+bot_name+']*[\s\?]*(舔|赞|顶|捧|夸|谢谢|感谢).+', msg_content):
            content_name = re.match(r'^['+bot_name+']*[\s\?]*(舔|赞|顶|捧|夸|谢谢|感谢)(.+)',
                                    msg_content).group(2).replace("@", "").replace("?", "")
            response = requests.get("https://chp.shadiao.app/api.php")
            wx_inst.send_text(from_chatroom_wxid,
                              "@{}  {}".format(content_name, response.text))
            return

    # ######################################################################################################==>>>vip群组功能
    if data_type[0] == '1' and (from_chatroom_wxid in BotService.get_config_val_obj("group_vip_list")):
        if re.match(r'^['+bot_name+']+[\s\?]+(我是色批|来张色图|我要看图片)', msg_content):
            randomImg = randomFile(isLoad=False)
            wx_inst.send_img(from_chatroom_wxid, randomImg)
            return
    # ######################################################################################################==>>>supvip群组功能
    if data_type[0] == '1' and (from_chatroom_wxid in BotService.get_config_val_obj("group_supvip_list")):
        if re.match(r'^['+bot_name+']+[\s\?]+(我是色批|来张色图|我要看图片)', msg_content):
            randomImg = randomFile(isLoad=False)
            wx_inst.send_img(from_chatroom_wxid, randomImg)
            return
    # #######################################################################################################==>>>普通群组功能
    if data_type[0] == '1' and (from_chatroom_wxid in BotService.get_config_val_obj("group_receive_list")):
        # 查看撤回的消息
        if re.match(r'^['+bot_name+']*[\s\?]*查看前面第\d+条消息', msg_content):
            content_name = re.match(r'^['+bot_name+']*[\s\?]*查看前面第(\d+)条消息',
                                    msg_content).group(1).replace("@", "").replace("?", "")
            num = int(content_name)
            msg_obj = botService.getChatroomMsg(
                from_chatroom_wxid=from_chatroom_wxid, num=num)
            msg = "消息未找到!"
            if msg_obj.exists():
                msg = "消息："+msg_obj.first()["msg"]
            wx_inst.send_text(from_chatroom_wxid, msg)
            return
        if re.match(r'^['+bot_name+']*[\s\?]*.*消息.*', msg_content):
            wx_inst.send_text(from_chatroom_wxid, "查看消息命令：查看前面第n条消息")
            return
        # 群舔人
        if re.match(r'^['+bot_name+']*[\s\?]*(舔|赞|顶|捧|夸|谢谢|感谢).+', msg_content):
            content_name = re.match(r'^['+bot_name+']*[\s\?]*(舔|赞|顶|捧|夸|谢谢|感谢)(.+)',
                                    msg_content).group(2).replace("@", "").replace("?", "")
            response = requests.get("https://chp.shadiao.app/api.php")
            wx_inst.send_text(from_chatroom_wxid,
                              "@{}  {}".format(content_name, response.text))
        elif re.match(r'^['+bot_name+']*[\s\?]*.+[你]*真(棒|强|厉害|牛逼)', msg_content):
            content_name = re.match(r'^['+bot_name+']**[\s\?]*(.+)[你]*真[棒,强,厉害,牛逼]+', msg_content).group(
                1).replace("@", "").replace("你", "").replace("?", "")
            response = requests.get(
                "https://chp.shadiao.app/api.php")
            wx_inst.send_text(
                from_chatroom_wxid, "@{}  {}".format(content_name, response.text))
        # 群骂人（仅管理员）
        elif re.match(r'^['+bot_name+']*[\s\?]*(喷|骂)+.+', msg_content):
            if from_wxid != admin_wx:
                wx_inst.send_text(from_chatroom_wxid, "命令您没权限！")
            content_name = re.match(
                r'^['+bot_name+']*[\s\?]*[喷,骂]+(.+)', msg_content).group(1).replace("@", "").replace("?", "")
            response = requests.get(
                "https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn")
            wx_inst.send_text(
                from_chatroom_wxid, "@{}  {}".format(content_name, response.text))
        # 群点歌
        elif re.match(r'^['+bot_name+']*[\s\?]*点歌.+', msg_content):
            content_text = re.match(
                r'['+bot_name+']*[\s\?]*点歌(.+)', msg_content).group(1).replace("@", "").replace("?", "")
            response = requests.get(
                "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=1&w="+content_text+"&format=json")
            text_json = json.loads(response.text)
            if text_json.get("data", {}).get("song").get("totalnum") <= 0:
                wx_inst.send_text(
                    from_chatroom_wxid, "未找到歌曲【"+content_text+"】")
            obj = text_json.get("data", {}).get(
                "song", {}).get("list", {})[0]
            albummid = obj.get(
                "albummid", "002vVK9r4dRzPY")
            if albummid == "":
                albummid = "002vVK9r4dRzPY"
            wx_inst.send_link_card(from_chatroom_wxid, obj.get("songname"), obj.get("singer")[0].get("name"), "https://y.qq.com/n/yqq/song/"+obj.get(
                "songmid", "")+".html", img_url='https://y.gtimg.cn/music/photo_new/T002R300x300M000'+albummid+'_1.jpg?max_age=2592000')

        # 群帮助
        elif re.match(r'^['+bot_name+']+[\s\?]+(help|帮助)', msg_content):
            help_msg = '''赞某人：舔xx，赞xx，顶xx，捧xx，夸xx,xx真棒，xx真强，xx真厉害，xx真牛逼
                            天气：@bot天气深圳
                            中英翻译：@bot翻译i love you
                            智能聊天：@bot你好
                            笑话：@bot笑话
                            歌词⑴：@bot歌词后来
                            歌词⑵：@bot歌词后来-刘若英
                            计算⑴：@bot计算1+1*2/3-4
                            计算⑵：@bot1+1*2/3-4
                            ＩＰ⑴：@bot归属127.0.0.1
                            ＩＰ⑵：@bot127.0.0.1
                            手机⑴：@bot归属13430108888
                            手机⑵：@bot13430108888
                            成语查询：@bot成语一生一世
                            五笔/拼音：@bot好字的五笔/拼音'''
            wx_inst.send_text(from_chatroom_wxid, "{}".format(help_msg))
        # 随机聊天
        elif re.match(r'^'+bot_name+'+[\?]*.*', msg_content):
            to_my_msg = msg_content.replace(
                bot_name+"?", '').replace(bot_name+" ", '')
            response = requests.get(
                "http://api.qingyunke.com/api.php?key=free&appid=0&msg="+to_my_msg)
            wx_inst.send_text(from_chatroom_wxid, "{}".format(json.loads(
                response.text).get('content', '').replace('{br}', '\n')))
    pass  # end
    print('未通过msg===>:', msg_content)
