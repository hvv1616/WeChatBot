from os import times
from .models import *
from django.db.models import F, Q
from decimal import Decimal
from django.conf import settings
from django.core.cache import caches
from django.db import connection
import json
import threading
from django.core.paginator import Paginator,Page #导入模块

class BotService():
    bot_config = None
    """
    初始化
    """

    def __init__(self, bot_wxid):
        self.bot_wxid = bot_wxid
        pass

    @staticmethod
    def load_bot_config(bot_wxid):
        """
        加载bot配置的静态方法
        """      
        if BotService.bot_config == None:
            kwargs={}
            if bot_wxid:
                kwargs["bot_wxid"]=bot_wxid
            BotService.bot_config = BotConfig.objects.filter(**kwargs).values()
            print("初始化加载bot配置======>", BotService.bot_config)

    @staticmethod
    def get_config_val(key):
        """
        获取配置值
        """
        try:
            if BotService.bot_config == None:
                BotService.load_bot_config(None)
            obj=list(filter((lambda x: x["key"] == key), BotService.bot_config)).pop()
            if obj:
                return obj["val"]
            else:
                return None
        except Exception as e:
            return ""

    @staticmethod
    def get_config_val_obj(key):
        return json.loads(BotService.get_config_val(key))

    def init_bot_data(self):
        """
        初始化bot配置数据
        """
        with connection.cursor() as cursor:
            sql_list = """
            update "main"."bot_config" set bot_wxid=strftime('%Y-%m-%d %H:%M:%f deleted','now') where bot_wxid='{bot_wxid}'
            INSERT INTO "main"."bot_config"("bot_wxid", "val_type", "key", "val", "desc") VALUES (92, '{bot_wxid}', 'string', 'bot_wxid', '{bot_wxid}', '机器人微信id');
            INSERT INTO "main"."bot_config"("bot_wxid", "val_type", "key", "val", "desc") VALUES ('{bot_wxid}', 'string', 'bot_name', '天天bot', '机器人微信名称');
            INSERT INTO "main"."bot_config"("bot_wxid", "val_type", "key", "val", "desc") VALUES ('{bot_wxid}', 'array', 'group_receive_list', '["xxx@chatroom"]', '群组接受名单');
            INSERT INTO "main"."bot_config"("bot_wxid", "val_type", "key", "val", "desc") VALUES ('{bot_wxid}', 'array', 'group_vip_list', '["xxx@chatroom"]', 'vip群组接受名单');
            INSERT INTO "main"."bot_config"("bot_wxid", "val_type", "key", "val", "desc") VALUES ('{bot_wxid}', 'array', 'group_supvip_list', '["xxx@chatroom"]', 'supvip群组接受名单');
            INSERT INTO "main"."bot_config"("bot_wxid", "val_type", "key", "val", "desc") VALUES ('{bot_wxid}', 'array', 'single_block_list', '["wxid_xxxx"]', '单人黑名单列表');
            INSERT INTO "main"."bot_config"("bot_wxid", "val_type", "key", "val", "desc") VALUES ('{bot_wxid}', 'array', 'group_test_list', '["xxx@chatroom"]', '测试群组接受名单');
            INSERT INTO "main"."bot_config"("bot_wxid", "val_type", "key", "val", "desc") VALUES ('{bot_wxid}', 'array', 'group_back_list', '["xxx@chatroom"]', '黑名单群组');
            """.format(bot_wxid=self.bot_wxid).split(";")[:-1]
            for x in sql_list:
                print('执行===》'+x)
                cursor.execute(x)
        pass

    def reload_bot_config(self):
        """
        重新加载bot配置
        """
        BotService.bot_config = BotConfig.objects.filter(
            Q(bot_wxid=self.bot_wxid)).values()
        print("重新加载bot配置======>", BotService.bot_config)

    def del_bot_data(self):
        """
        初始化bot配置数据
        """
        with connection.cursor() as cursor:
            sql_list = """
             delete from "main"."bot_config" where bot_wxid='{bot_wxid}';
             """.format(bot_wxid=self.bot_wxid).split(";")[:-1]
            for x in sql_list:
                print('执行===》'+x)
                cursor.execute(x)
        pass

    def addAdminWX(self, admin_wx):
        """
        添加管理员微信
        """
        bot_wxid = self.bot_wxid
        entitys = BotConfig.objects.filter(
            Q(bot_wxid=bot_wxid) & Q(key='admin_wx')).values()
        print(entitys)
        if entitys.count() == 0:
            self.init_bot_data()
            botConfig = BotConfig(
                bot_wxid=bot_wxid, val_type="string", key="admin_wx", val=admin_wx, desc="控制台微信id")
            botConfig.save()
            self.reload_bot_config()
            return True
        else:
            return False
        pass

    def arrayConfigAdd(self, key, addVal):
        """
        数组配置，添加值
        """
        entitys = BotConfig.objects.filter(
            Q(bot_wxid=self.bot_wxid) & Q(key=key)).values()
        if entitys.count() > 0:
            item = entitys.first()
            val_arr = json.loads(item["val"])
            val_arr.append(addVal)
            BotConfig.objects.filter(id=item["id"]).update(
                val=json.dumps(val_arr, ensure_ascii=False))
            self.reload_bot_config()
        pass

    def arrayConfigDel(self, key, delVal):
        """
        数组配置，删除值
        """
        entitys = BotConfig.objects.filter(
            Q(bot_wxid=self.bot_wxid) & Q(key=key)).values()
        if entitys.count() > 0:
            item = entitys.first()
            val_arr = json.loads(item["val"])
            val_arr = list(filter(lambda x: not x == delVal, val_arr))
            BotConfig.objects.filter(id=item["id"]).update(
                val=json.dumps(val_arr, ensure_ascii=False))
            self.reload_bot_config()
        pass
    def getChatroomMsg(self,from_chatroom_wxid,num):
        """
        获取前面第几条消息
        """
        msg_list=BotChatroomMsg.objects.filter(
                from_chatroom_wxid=from_chatroom_wxid).order_by("-id")[num:num+1].values()
        return msg_list
        # paginator = Paginator(msg_list,1)
        # res_list = paginator.page(number=num)
        # print(res_list)
        # return res_list.object_list.first()
        
    def saveMsg(self, msg):
        """
        保存消息
        """
        #BotService.saveMsgByDB(msg)
        #threading.Thread(target=BotService.saveMsgByDB, args=(msg,)).start()
        pass

    @staticmethod
    def saveMsgByDB(message):
        bot_wxid = message.get('user', 'bot_wxid')
        if 'msg::single' in message.get('type'):
            good_friend_msg_obj = BotGoodFriendMsg(
                bot_wxid=bot_wxid,
                data_type=message.get('data', {}).get('data_type', ''),
                send_or_recv=message.get('data', {}).get('send_or_recv', ''),
                from_wxid=message.get('data', {}).get('from_member_wxid', ''),
                from_nickname=message.get('data', {}).get('from_nickname', ''),
                time=message.get('data', {}).get('time', ''),
                msg=message.get('data', {}).get('msg', ''),
                desc='',
            )
            good_friend_msg_obj.save()
            pass
        elif 'msg::chatroom' in message.get('type'):
            bot_chat_room_msg = BotChatroomMsg(
                bot_wxid=bot_wxid,
                data_type=message.get('data', {}).get('data_type', ''),
                send_or_recv=message.get('data', {}).get('send_or_recv', ''),
                from_chatroom_wxid=message.get(
                    'data', {}).get('from_chatroom_wxid', ''),
                from_chatroom_nickname=message.get(
                    'data', {}).get('from_chatroom_nickname', ''),
                from_member_wxid=message.get(
                    'data', {}).get('from_member_wxid', ''),
                time=message.get('data', {}).get('time', ''),
                msg=message.get('data', {}).get('msg', ''),
                desc='',
            )
            bot_chat_room_msg.save()
            pass
        elif 'friend::chatroom' in message.get('type'):
            entity = BotChatroom.objects.filter(
                chatroom_id=message.get('data', {}).get('chatroom_id', ''))
            if not entity.exists():
                bot_chat_room = BotChatroom(
                    bot_wxid=bot_wxid,
                    chatroom_id=message.get('data', {}).get('chatroom_id', ''),
                    chatroom_name=message.get(
                        'data', {}).get('chatroom_name', ''),
                    chatroom_avatar=message.get(
                        'data', {}).get('chatroom_avatar', ''),
                    desc='',
                )
                bot_chat_room.save()
            pass
        elif 'friend::person' in message.get('type'):
            entity = BotGoodFriend.objects.filter(
                wx_id=message.get('data', {}).get('wx_id', ''))
            if not entity.exists():
                bot_good_friend = BotGoodFriend(
                    bot_wxid=bot_wxid,
                    wx_id=message.get('data', {}).get('wx_id', ''),
                    wx_id_search=message.get(
                        'data', {}).get('wx_id_search', ''),
                    wx_nickname=message.get('data', {}).get('wx_nickname', ''),
                    wx_avatar=message.get('data', {}).get('wx_avatar', ''),
                    remark_name=message.get('data', {}).get('remark_name', ''),
                    desc='',
                )
                bot_good_friend.save()
            pass
    pass
