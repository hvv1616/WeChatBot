# 启动项目
```
# 初始化安装包
pip freeze >requirements.txt
# 安装安装包
pip install -r requirements.txt
# 启动web项目
python manage.py runserver
#创建管理员账号
python manage.py createsuperuser
#重置数据库
python manage.py flush
# 添加models
python manage.py migrate
# 变更models
python manage.py makemigrations
# 安装window操作包 Windows - pywin32, pyHook
    #安装PyMouse包的window插件，cmd进入lib文件夹，运行
    pip install pyHook-1.5.1-cp37-cp37m-win_amd64.whl
    pip install PyUserinput
```