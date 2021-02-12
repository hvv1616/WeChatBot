from django.contrib import admin
from .models import BotCommand,BotConfig

# class BotCommandAdmin(admin.ModelAdmin):
#     list_display = ["bot_wxid", "reg", "desc", "scope_wxid", "scope_group"]


class BotConfigAdmin(admin.ModelAdmin):
    list_display = ["bot_wxid", "val_type", "key", "val", "desc"]
    
#admin.site.register(BotCommand,BotCommandAdmin)
admin.site.register(BotConfig,BotConfigAdmin)