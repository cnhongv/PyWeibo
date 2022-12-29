from django.contrib import admin

# Register your models here.
from .models import User, Weibo, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ('uid', 'uin', 'pwd', 'nick', 'email',
                    'avatar', 'utype', 'reg_time', 'last_login')


class WeiboAdmin(admin.ModelAdmin):
    list_display = ('wid', 'uid', 'text', 'time', 'wtype',
                    'view', 'like', 'comments', 'is_del')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('cid', 'wid', 'uid', 'text', 'time', 'is_del')


admin.site.register(User, UserAdmin)
admin.site.register(Weibo, WeiboAdmin)
admin.site.register(Comment, CommentAdmin)
