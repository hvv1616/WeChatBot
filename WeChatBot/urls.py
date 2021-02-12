"""
Definition of urls for WeChatBot.
"""

from datetime import datetime
from django.urls import path
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from apps.app import forms, views
import WeChatBot.bot_views as bot_views
from apps.bot import urls 
urlpatterns = [
    url(r'^bot/hello', bot_views.hello),
    # url(r'^bot_start/', botViews.start),
    # url(r'^onmessage/', botViews.onmessage),
    # url(r'^send_msg/', botViews.send_msg),
    path('bot/', include('apps.bot.urls')),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
   
]

