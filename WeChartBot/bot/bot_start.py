# coding: utf-8

from WechatPCAPI import WechatPCAPI
import time
import logging
from queue import Queue
import threading
import json
import msg_handler
import re
import requests
file_name = str(time.strftime("%Y-%m-%d", time.localtime()))+".log"
logging.basicConfig(filename=file_name, level=logging.INFO)
queue_recved_message = Queue()  # 用来处理所有消息
queue_groups = Queue()  # 用来处理群ID消息
queue_Members = Queue()  # 用来处理群成员信息


# 控制台微信
admin_wx = 'wxid_dg5xnz4s39ea21'
# 单人黑名单列表
single_block_list = ['wxid_xxxx']  # 最好把控制台微信加进去
# 群组接受名单
group_receive_list = [
                    #   "19162403962@chatroom",  # 测试1群
                    #   "17648533871@chatroom",  # 测试2群
                    #   "18162133106@chatroom",  # 大娃去哪了
                    #   "5581512142@chatroom",  # 顺其自然
                    #   "7165888394@chatroom",  # 家人2（年轻人）
                    #   "7029811144@chatroom",  # 人类精英交流群
                    #   "20209106528@chatroom",  # SC中台组
                    #   '20086915165@chatroom',  # 鲧禹中台大群
                      ]
# 创建remark_name字典
dict_remark_name = {}
# 定义信息ID字典
dict_msg_ID = {}
# 全局
ID_num = 0


class Person:
    def __init__(self):
        self.chatroom_id = ""
        self.wx_id = ""
        self.nick_name = ""


def onmessage(message):
    print('onmessage', message)
    queue_recved_message.put(message)


# def thead_handle_mess(wx_inst):
#     while True:
#         time.sleep(1)
#         if not queue_recved_message.empty():
#             message = queue_recved_message.get()
#             if 'friend::chatroom' in message.get('type'):
#                 if chatroom in message.get('data', {}).get('chatroom_name', ""):
#                     queue_groups.put(message.get(
#                     'data', {}).get('chatroom_id', ""))
#             elif 'member::chatroom' in message.get('type'): #新成员加入
#                 Per = Person()  # 生成新的对象
#                 Per.chatroom_id = message.get(
#                     'data', {}).get('chatroom_id', "")
#                 Per.wx_id = message.get('data', {}).get('wx_id', "")
#                 Per.nick_name = message.get('data', {}).get('wx_nickname', "")
#                 queue_Members.put(Per)
#             elif 'msg::chatroom' in message.get('type'): #收到消息

# 消息处理 分流
def thread_handle_message(wx_inst):
    global ID_num
    while True:
        message = queue_recved_message.get()
        print(message)

        # 坑点: if和elif 慎用

        # 本地保存friends信息, 重点remark_name
        try:
            if 'friend::person' in message.get('type'):
                deal_remark_name(message)
        except:
            pass

        # 单人消息
        try:
            if 'msg::single' in message.get('type'):
                # 这里是判断收到的是消息 不是别的响应
                send_or_recv = message.get('data', {}).get('send_or_recv', '')
                # 判断微信id, 黑名单
                from_wxid = message.get('data', {}).get('from_wxid', '')
                data_type = message.get('data', {}).get('data_type', '')
                if send_or_recv[0] == '0':
                    # 0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复

                    if (from_wxid not in single_block_list) and (from_wxid in dict_remark_name.keys()):
                        # 判断微信id, 黑名单, 并且屏蔽公众号
                        if data_type[0] == '1':
                            # 只接受文字
                            msg_content = message.get(
                                'data', {}).get('msg', '')
                            wx_inst.send_text(admin_wx, '微信收到好友消息\n  {} : {} \n信息ID {}'.format(
                                dict_remark_name[from_wxid], msg_content, ID_num))
                        else:
                            wx_inst.send_text(admin_wx, '微信收到好友{}一张图片或表情包 \n信息ID {}'.format(
                                dict_remark_name[from_wxid], ID_num))

                        # 弄一个字典, 保存信息ID, 通过回复ID+信息进行回复给好友
                        dict_msg_ID[ID_num] = from_wxid
                        ID_num = ID_num + 1

                # 进行回复
                if (send_or_recv[0] == '0') and (from_wxid in admin_wx):
                    msg_content = message.get('data', {}).get('msg', '')
                    try:
                        reply_msage_ID = msg_content.split(' ', 1)[0]
                        reply_msage = msg_content.split(' ', 1)[1]

                        # print(dict_msg_ID[int(reply_msage_ID)])
                        # print(type(dict_msg_ID[reply_msage_ID]))
                        # print(reply_msage)
                        # print(type(reply_msage))

                        wx_inst.send_text(
                            str(dict_msg_ID[int(reply_msage_ID)]), str(reply_msage))
                    except:
                        wx_inst.send_text(admin_wx, '没事干控制端不要发信息')
        except:
            pass

        # 接受群组信息
        try:
            if 'msg::chatroom' in message.get('type'):
                # 这里是判断收到的是消息 不是别的响应
                send_or_recv = message.get('data', {}).get('send_or_recv', '')
                data_type = message.get('data', {}).get('data_type', '')
                # 判断群组id, 黑名单
                from_chatroom_wxid = message.get(
                    'data', {}).get('from_chatroom_wxid', '')
                print('接受群组信息1:', group_receive_list,
                      (from_chatroom_wxid in group_receive_list), send_or_recv, send_or_recv[0])
                
                if send_or_recv[0] == '0':
                    if from_chatroom_wxid in group_receive_list:
                        print('接受群组信息2:', send_or_recv,
                              send_or_recv[0], 'from_chatroom_wxid', from_chatroom_wxid, 'data_type[0] :', data_type[0])
                        if data_type[0] == '1':
                            msg_content = message.get(
                                'data', {}).get('msg', '')
                            from_wxid = message.get('data', {}).get(
                                'from_member_wxid', '')
                            from_chatroom_wxid = message.get(
                                'data', {}).get('from_chatroom_wxid', '')
                            from_chatroom_nickname = message.get(
                                'data', {}).get('from_chatroom_nickname', '')
                            #wx_inst.send_text(admin_wx, '微信收到群 {} 消息\n {} : {}  \n信息ID {}'.format(from_chatroom_nickname,dict_remark_name.get(from_wxid, from_wxid), msg_content, ID_num))
                            if re.match(r'^[舔,赞,顶,捧,夸]+.+', msg_content):
                                content_name = re.match(
                                    r'^[舔,赞,顶,捧,夸]+(.+)', msg_content).group(1).replace("@", "").replace("?", "")
                                response = requests.get(
                                    "https://chp.shadiao.app/api.php")
                                wx_inst.send_text(
                                    from_chatroom_wxid, "@{}  {}".format(content_name, response.text))
                            elif re.match(r'^.+[你]*真[棒,强,厉害,牛逼]+', msg_content):
                                content_name = re.match(r'^(.+)[你]*真[棒,强,厉害,牛逼]+', msg_content).group(
                                    1).replace("@", "").replace("你", "").replace("?", "")
                                response = requests.get(
                                    "https://chp.shadiao.app/api.php")
                                wx_inst.send_text(
                                    from_chatroom_wxid, "@{}  {}".format(content_name, response.text))
                            
                            elif re.match(r'点歌.+', msg_content):
                                content_text = re.match(
                                    r'点歌(.+)', msg_content).group(1).replace("@", "").replace("?", "")
                                print("点歌：", content_text)
                                response = requests.get(
                                    "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&n=1&w="+content_text+"&format=json")
                                text_json = json.loads(response.text)
                                print("text_json：", text_json)
                                if text_json.get("data", {}).get("song").get("totalnum") <= 0:
                                    wx_inst.send_text(
                                        from_chatroom_wxid, "未找到歌曲【"+content_text+"】")
                                obj = text_json.get("data", {}).get(
                                    "song", {}).get("list", {})[0]
                                print("obj:", obj)
                                albummid = obj.get(
                                    "albummid", "002vVK9r4dRzPY")
                                if albummid == "":
                                    albummid = "002vVK9r4dRzPY"
                                wx_inst.send_link_card(from_chatroom_wxid, obj.get("songname"), obj.get("singer")[0].get("name"), "https://y.qq.com/n/yqq/song/"+obj.get(
                                    "songmid", "")+".html", img_url='https://y.gtimg.cn/music/photo_new/T002R300x300M000'+albummid+'_1.jpg?max_age=2592000')
                            elif re.match(r'^[喷,骂]+.+', msg_content) and from_wxid == admin_wx:
                                # https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn
                                content_name = re.match(
                                    r'^[喷,骂]+(.+)', msg_content).group(1).replace("@", "").replace("?", "")
                                response = requests.get(
                                    "https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn")
                                wx_inst.send_text(
                                    from_chatroom_wxid, "@{}  {}".format(content_name, response.text))
                                                             
                            elif re.match(r'[help,帮助]+.*@天天bot[\?]*[help,帮助]+', msg_content):
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
                                wx_inst.send_text(
                                    from_chatroom_wxid, "{}".format(help_msg))
                            elif re.match(r'.*@天天bot[\?]*.*', msg_content):
                                to_my_msg = re.match(
                                    r'(.*)@天天bot[\?]*(.*)', msg_content).group(1) + re.match(
                                    r'(.*)@天天bot[\?]*(.*)', msg_content).group(2)
                                print(to_my_msg)
                                response = requests.get(
                                    "http://api.qingyunke.com/api.php?key=free&appid=0&msg="+to_my_msg)
                                print(response.text)
                                wx_inst.send_text(
                                    from_chatroom_wxid, "{}".format(json.loads(response.text).get('content', '').replace('{br}', '\n')))
                        else:
                            from_wxid = message.get('data', {}).get(
                                'from_member_wxid', '')
                            from_chatroom_wxid = message.get(
                                'data', {}).get('from_chatroom_wxid', '')
                            from_chatroom_nickname = message.get(
                                'data', {}).get('from_chatroom_nickname', '')
                            wx_inst.send_text(admin_wx, '微信收到群 {} 消息成员{} \n一张图片/表情   \n信息ID {}'.format(from_chatroom_nickname,
                                                                                                       dict_remark_name[from_wxid], ID_num))

                        # 弄一个字典, 保存信息ID, 通过回复ID+信息进行回复给好友
                        dict_msg_ID[ID_num] = from_chatroom_wxid
                        ID_num = ID_num + 1
                    ## 不在权限群组的消息
                    else:
                        if data_type[0] == '1':
                            msg_content = message.get(
                            'data', {}).get('msg', '')
                            from_wxid = message.get('data', {}).get(
                                'from_member_wxid', '')
                            from_chatroom_wxid = message.get(
                                'data', {}).get('from_chatroom_wxid', '')
                            from_chatroom_nickname = message.get(
                            'data', {}).get('from_chatroom_nickname', '')
                            ## 所有群组权限
                            if re.match(r'^[添加群组]+', msg_content) and from_wxid == admin_wx :
                                msg_content = message.get('data', {}).get('msg', '')
                                from_wxid = message.get('data', {}).get('from_member_wxid', '')
                                from_chatroom_wxid = message.get('data', {}).get('from_chatroom_wxid', '')
                                from_chatroom_nickname = message.get('data', {}).get('from_chatroom_nickname', '')
                                from_chatroom_nickname = message.get('data', {}).get('from_chatroom_nickname', '')
                                #global group_receive_list
                                print('添加群组0',from_chatroom_wxid)
                                group_receive_list.append(from_chatroom_wxid)
                                print('添加群组1',group_receive_list,{from_chatroom_wxid:from_chatroom_nickname})
                                add_group_receive_config({from_chatroom_wxid:from_chatroom_nickname})
                                print('添加群组2',{from_chatroom_wxid:from_chatroom_nickname})
                                wx_inst.send_text(from_chatroom_wxid, "群组【"+from_chatroom_nickname+"】添加成功！") 

        except Exception as e:
            print(e, '消息处理失败!', message)
            pass


def thead_handle_getmember(wx_inst, Group_list):
    while True:
        for group in Group_list:
            wx_inst.get_member_of_chatroom(group)
        time.sleep(60)

# 获取队列


def get_group_list():
    Group_list = []
    while queue_groups.empty():
        time.sleep(1)
    while not queue_groups.empty():
        Group_list.append(queue_groups.get())
    return Group_list


def get_existed_member(wx_inst, Group_list):
    member_groups = {}
    for group in Group_list:
        wx_inst.get_member_of_chatroom(group)
    while queue_Members.empty():
        time.sleep(0.5)
    while not queue_Members.empty():
        Person = queue_Members.get()
        if Person.chatroom_id not in member_groups.keys():
            member_group = {Person.chatroom_id: [Person]}
            member_groups.update(member_group)
        elif Person.wx_id not in get_all_id(member_group[Person.chatroom_id]):
            member_group[Person.chatroom_id].append(Person)
    return member_groups


def thread_handle_member_welcome(wx_inst, member_groups):
    groups = member_groups
    with open('config.json', 'r')as f:
        j = json.loads(f.read())
    mess = j['mess']
    while True:
        if not queue_Members.empty():
            Person = queue_Members.get()
            if Person.wx_id not in get_all_id(groups[Person.chatroom_id]):

                add_member(Person, groups)
                try:
                    wx_inst.send_text(to_user=Person.chatroom_id,
                                      msg=mess, at_someone=Person.wx_id)
                except Exception as e:
                    print(e)
                print("Say welcome to {}".format(Person.nick_name))
            else:
                pass
        else:
            pass


def get_config_path():
    return 'D:\Project\Bot\WechatPCAPI\WeChartBot\\bot\config.json'


def add_group_receive_config(dic):
    path = get_config_path()
    try:
        f = open(get_config_path(), "rb")
        j = json.loads(f.read())
        j.get('group_receive_list_dic', [{}]).append(dic)
        f.close()
        config_writer(json.dumps(j,ensure_ascii=False))
    except Exception as e:
        print(e)


def config_writer(txt):
    f = open(get_config_path(), "w" ,encoding='utf-8')
    f.write(txt)
    f.close()


def load_config():
    path = get_config_path()
    print(path)
    # while True:
    try:
        with open(path, 'rb') as f:
            # # 控制台微信
            # admin_wx = 'wxid_dg5xnz4s39ea21'
            # # 单人黑名单列表
            # single_block_list = ['wxid_xxxx']  # 最好把控制台微信加进去
            # # 群组接受名单
            # group_receive_list = ['19162403962@chatroom']
            # # 创建remark_name字典
            # dict_remark_name = {}
            # # 定义信息ID字典
            # dict_msg_ID = {}
            j = json.loads(f.read())
            global admin_wx
            admin_wx = j.get('admin_wx', 'wxid_dg5xnz4s39ea21')
            global single_block_list
            single_block_list = j.get('single_block_list', ['wxid_xxxx'])
           # global group_receive_list
            for item in  j.get('group_receive_list_dic', [{}]):
                group_receive_list.append(list(item.keys())[0])
            #group_receive_list = j.get('group_receive_list_dic', [{}]).keys()
            print(group_receive_list)
            global dict_remark_name
            dict_remark_name = j.get('dict_remark_name', {})
            global dict_msg_ID
            dict_msg_ID = j.get('dict_msg_ID', {})
            print('重新加载配置：', j)
            print("配置打印",admin_wx, single_block_list, group_receive_list,
                  dict_remark_name, dict_msg_ID)
            #time.sleep(10)
    except Exception as e:
        print(e)


def main():
    print("初始化中...请稍候！")
    # threading.Thread(target=load_config,
    #                  args=()).start()
    # print("配置加载完成！")
    load_config()
    wx_inst = WechatPCAPI(on_message=onmessage)
    wx_inst.start_wechat(block=True)
    time.sleep(3)
   # threading.Thread(target=thead_handle_mess, args=(wx_inst,)).start()
    threading.Thread(target=thread_handle_message, args=(wx_inst,)).start()
    wx_inst.update_frinds()
    Group_list = get_group_list()
    member_groups = get_existed_member(wx_inst, Group_list)
    print("运行中....")
    threading.Thread(target=thead_handle_getmember,
                     args=(wx_inst, Group_list,)).start()
    return wx_inst
    # threading.Thread(target=thread_handle_member_welcome,
    #                  args=(wx_inst, member_groups,)).start()


def get_all_id(List):
    id_list = []
    for i in List:
        id_list.append(i.wx_id)
    return id_list


def add_member(Person, member_groups):
    member_groups[Person.chatroom_id].append(Person)


if __name__ == "__main__":
    main()
