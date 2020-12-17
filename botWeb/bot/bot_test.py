# coding: utf-8
import unittest
import os
import json
import bot
import threading
import time
#from bot import bot
import re

class TestDict(unittest.TestCase):
    def test_ex(self):
        path='D:\Project\Bot\WechatPCAPI\src\config.json'
        print(path)
        with open(path, 'rb') as f:
            j = json.loads(f.read())
            print(j,j["group_id_arr"])
            threading.Thread(target=bot.thead_handle_mess, args=({},)).start()
            bot.onmessage(j["test_msg"])
            time.sleep(2)
            
            print(json.dumps(bot.queue_groups))
            # self.assertEqual('B', 'A')
            # msg = {'user': 'wxid_kkp102awseir22', 'type': 'msg::chatroom',
            #     'data': {'data_type': '1', 'send_or_recv': '0+[收到]', 'from_chatroom_wxid': '19162403962@chatroom',
            #                 'from_member_wxid': 'wxid_dg5xnz4s39ea21', 'time': '2020-12-12 08:46:04', 'msg': '测试消息test111', 'from_chatroom_nickname': '测试群'}
            #     }

    # def test_80_to_100(self):
    #     s1 = Student('Bart', 80)
    #     s2 = Student('Lisa', 100)
    #     self.assertEqual(s1.get_grade(), 'A')
    #     self.assertEqual(s2.get_grade(), 'A')

    # def test_60_to_80(self):
    #     s1 = Student('Bart', 60)
    #     s2 = Student('Lisa', 79)
    #     self.assertEqual(s1.get_grade(), 'B')
    #     self.assertEqual(s2.get_grade(), 'B')

    # def test_0_to_60(self):
    #     s1 = Student('Bart', 0)
    #     s2 = Student('Lisa', 59)
    #     self.assertEqual(s1.get_grade(), 'C')
    #     self.assertEqual(s2.get_grade(), 'C')

    # def test_invalid(self):
    #     s1 = Student('Bart', -1)
    #     s2 = Student('Lisa', 101)
    #     with self.assertRaises(ValueError):
    #         s1.get_grade()
    #     with self.assertRaises(ValueError):
    #         s2.get_grade()

if __name__ == '__main__':
    unittest.main()
