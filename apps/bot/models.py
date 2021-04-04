from django.db import models

class BotCommand(models.Model):
    bot_wxid = models.CharField(max_length=255, default='', blank=False, verbose_name='机器人微信id')
    reg = models.CharField(max_length=255, default='', blank=False, verbose_name='命令的正则表达式')
    desc = models.CharField(max_length=255, default='', blank=False, verbose_name='命令功能等描述')
    scope_wxid = models.CharField(max_length=4000, default='', blank=False, verbose_name='限定微信id范围，多个用,隔开')
    scope_group = models.CharField(max_length=4000, default='', blank=False, verbose_name='限定微信群组id范围，多个用,隔开')
    class Meta:
        db_table = 'bot_command'
        verbose_name = '机器人命令表'
        verbose_name_plural = verbose_name

class BotConfig(models.Model):
    bot_wxid = models.CharField(max_length=255, default='', blank=False, verbose_name='机器人微信id')
    val_type = models.CharField(max_length=255, default='', blank=False, verbose_name='配置的值类型（string字符串,array数组,object对象）')
    key = models.CharField(max_length=255, default='', blank=False, verbose_name='配置唯一key')
    val = models.CharField(max_length=4000, default='', blank=False, verbose_name='值')
    desc = models.CharField(max_length=4000, default='', blank=False, verbose_name='配置描述')
    class Meta:
        db_table = 'bot_config'
        verbose_name = '机器人配置表'
        verbose_name_plural = verbose_name

class BotChatroom(models.Model):
    bot_wxid = models.CharField(max_length=255, default='', blank=False, verbose_name='机器人微信id')
    chatroom_id = models.CharField(max_length=255, default='', blank=False, verbose_name='群组id')
    chatroom_name = models.CharField(max_length=255, default='', blank=False, verbose_name='群组名称')
    chatroom_avatar = models.CharField(max_length=4000, default='', blank=False, verbose_name='群组头像')
    desc = models.CharField(max_length=4000, default='', blank=False, verbose_name='备注')
    class Meta:
        db_table = 'bot_chatroom'
        verbose_name = '机器人群组信息'
        verbose_name_plural = verbose_name
class BotGoodFriend(models.Model):
    bot_wxid = models.CharField(max_length=255, default='', blank=False, verbose_name='机器人微信id')
    wx_id = models.CharField(max_length=255, default='', blank=False, verbose_name='微信id')
    wx_id_search = models.CharField(max_length=255, default='', blank=False, verbose_name='好友微信id')
    wx_nickname = models.CharField(max_length=255, default='', blank=False, verbose_name='好友微信昵称')
    wx_avatar = models.CharField(max_length=4000, default='', blank=False, verbose_name='好友头像')
    remark_name = models.CharField(max_length=4000, default='', blank=False, verbose_name='好友微信备注名')
    desc = models.CharField(max_length=4000, default='', blank=False, verbose_name='备注')
    class Meta:
        db_table = 'bot_good_friend'
        verbose_name = '机器人好友'
        verbose_name_plural = verbose_name

class BotChatroomMsg(models.Model):
    bot_wxid = models.CharField(max_length=255, default='', blank=False, verbose_name='机器人微信id')
    data_type = models.CharField(max_length=255, default='', blank=False, verbose_name='消息类型，1:好友、群聊消息（判断微信id, 黑名单, 并且屏蔽公众号）')
    send_or_recv = models.CharField(max_length=255, default='', blank=False, verbose_name='接受类型（0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复）')
    from_chatroom_wxid = models.CharField(max_length=4000, default='', blank=False, verbose_name='消息来源群组id')
    from_chatroom_nickname = models.CharField(max_length=4000, default='', blank=False, verbose_name='消息来源群组昵称')
    from_member_wxid = models.CharField(max_length=4000, default='', blank=False, verbose_name='群组发送人id')
    time = models.CharField(max_length=20, default='', blank=False, verbose_name='时间')
    msg= models.CharField(max_length=8000, default='', blank=False, verbose_name='消息内容')
    desc = models.CharField(max_length=4000, default='', blank=False, verbose_name='备注')
    class Meta:
        db_table = 'bot_chatroom_msg'
        verbose_name = '群消息'
        verbose_name_plural = verbose_name
class BotGoodFriendMsg(models.Model):
    bot_wxid = models.CharField(max_length=255, default='', blank=False, verbose_name='机器人微信id')
    data_type = models.CharField(max_length=255, default='', blank=False, verbose_name='消息类型，1:好友、群聊消息（判断微信id, 黑名单, 并且屏蔽公众号）')
    send_or_recv = models.CharField(max_length=255, default='', blank=False, verbose_name='接受类型（0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复）')
    from_wxid = models.CharField(max_length=255, default='', blank=False, verbose_name='发送人id')
    from_nickname = models.CharField(max_length=4000, default='', blank=False, verbose_name='发送人昵称')
    time = models.CharField(max_length=20, default='', blank=False, verbose_name='时间')
    msg= models.CharField(max_length=8000, default='', blank=False, verbose_name='消息内容')
    desc = models.CharField(max_length=4000, default='', blank=False, verbose_name='备注')
    class Meta:
        db_table = 'bot_good_friend_msg'
        verbose_name = '好友消息'
        verbose_name_plural = verbose_name
class User(models.Model):
    # 管理员时使用账户密码登录
    username = models.CharField(max_length=32, default='', blank=True, verbose_name='用户账号')
    password = models.CharField(max_length=255, default='',blank=True, verbose_name='用户密码')
    mobile = models.CharField(max_length=11, default='', blank=True, verbose_name='用户手机号')
    email = models.EmailField(default='', blank=True, verbose_name='用户邮箱')
    real_name = models.CharField(max_length=16, default='', blank=True, verbose_name='真实姓名')
    id_num = models.CharField(max_length=18, default='', blank=True, verbose_name='身份证号')
    nick_name = models.CharField(max_length=32, default='', blank=True, verbose_name='昵称')
    region = models.CharField(max_length=255, default='', blank=True, verbose_name='地区')
    avatar_url = models.CharField(max_length=255, default='', blank=True, verbose_name='头像')
    open_id = models.CharField(max_length=255, default='', blank=True, verbose_name='微信openid') 
    union_id = models.CharField(max_length=255, default='', blank=True, verbose_name='微信unionid')
    gender = models.IntegerField(choices=((0, '未知'), (1, '男'), (2, '女')), default=0, verbose_name='性别')
    birth_date = models.DateField(verbose_name='生日', null=True, blank=True)
    is_freeze = models.IntegerField(default=0, choices=((0, '否'),(1, '是')),  verbose_name='是否冻结/是否封号')
    # is_admin = models.BooleanField(default=False, verbose_name='是否管理员')
  #  group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='用户组')
    # 组权分离后 当有权限时必定为管理员类型用户，否则为普通用户
  #  auth = models.ForeignKey(Auth, on_delete=models.PROTECT, null=True, blank=True, verbose_name='权限组') # 当auth被删除时，当前user的auth会被保留，但是auth下的auth_permissions会被删除，不返回
    bf_logo_time = models.DateTimeField(null=True, blank=True, verbose_name='上次登录时间')

    class Meta:
        db_table = 'A_User_Table'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

class BotChatActivity(models.Model):
    bot_wxid = models.CharField(max_length=255, default='', blank=True, verbose_name='机器人微信id')
    activity_type=models.CharField(max_length=1000, default='', blank=True, verbose_name='活动类型')
    from_member_wxid = models.CharField(max_length=100, default='', blank=True, verbose_name='发送人id')
    from_member_nickname = models.CharField(max_length=100, default='', blank=True, verbose_name='发送人微信名称')
    from_chatroom_wxid= models.CharField(max_length=100, default='', blank=True, verbose_name='群组id')
    from_chatroom_nickname= models.CharField(max_length=100, default='', blank=True, verbose_name='群组名称')
    login_username= models.CharField(max_length=100, default='', blank=True, verbose_name='登录用户名')
    login_req=models.CharField(max_length=4000, default='', blank=True, verbose_name='登录请求信息')
    login_res=models.CharField(max_length=4000, default='', blank=True, verbose_name='登录成功后响应体')
    token = models.CharField(max_length=4000, default='', blank=True, verbose_name='token')
    is_invalid = models.CharField(max_length=10, default='否', blank=True, verbose_name='是否失效（是，否）')
    sign_time = models.CharField(max_length=20, default='', blank=True, verbose_name='上次签到时间')
    sign_result = models.CharField(max_length=2000, default='', blank=True, verbose_name='上次签到结果')
    update_time = models.CharField(max_length=20, default='', blank=True, verbose_name='更新时间')
    create_time = models.CharField(max_length=20, default='', blank=True, verbose_name='创建时间')
    desc = models.CharField(max_length=4000, default='', blank=True, verbose_name='备注')
    
    class Meta:
        db_table = 'bot_activity'
        verbose_name = '活动登录信息消息'
        verbose_name_plural = verbose_name

