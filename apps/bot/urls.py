from datetime import datetime
from django.urls import path,re_path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from . import views
urlpatterns = [
    url(r'^test/', views.test),
    url(r'^verify_wx/', views.verify_wx),
    url(r'^start/', views.start),
    url(r'^onmessage/', views.onmessage),
    url(r'^get_chatroom_list/', views.get_chatroom_list),
    url(r'^send_trigger_text/', views.send_trigger_text),
    url(r'^send_text/', views.send_text),
    url(r'^send_link_card/', views.send_link_card),
    url(r'^send_img/', views.send_img),
    url(r'^send_file/', views.send_file),
    url(r'^mouse/', views.mouse),
    url(r'^signAll/', views.signAll),
    url(r'^getTimeImg/', views.getTimeImg),
    url(r'^downloadVideo/', views.downloadVideo),
    #path('bank/<str:key>/<str:title>/<str:body>/', views.bank_send_msg2),
    path('bank/<str:key>/<str:title>/<str:body>', views.bank_send_msg2),
    path('bank/<str:key>/<str:body>/', views.bank_send_msg1),
    path('bank/<str:key>/<str:body>', views.bank_send_msg1),
    re_path(r'^bank/(?P<key>[^/]+)/(?P<title>[^/]+)/(?P<body>[\s\S]+)$', views.bank_send_msg2),
    re_path(r'^bank/(?P<key>[^/]+)/(?P<body>[\s\S]+)$', views.bank_send_msg1),
]