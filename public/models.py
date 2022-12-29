import datetime
from django.utils import timezone
from django.db import models

# Create your models here.


class User(models.Model):
    uid = models.AutoField('用户唯一id', primary_key=True)  # 用户唯一id
    uin = models.CharField('用户名', max_length=20)     # 用户名
    pwd = models.CharField('密码', max_length=32)       # 用户密码
    nick = models.CharField('昵称', max_length=20)      # 用户昵称
    email = models.CharField('邮箱', max_length=32)     # 邮箱
    avatar = models.CharField('头像', max_length=256, default='')     # 头像
    utype = models.IntegerField('用户权限', default=0)  # 用户权限 0： 正常 1：禁言
    reg_time = models.DateTimeField('注册时间', auto_now_add=True)         # 用户注册时间
    last_login = models.DateTimeField('最后登录时间', auto_now_add=True)   # 用户最后登录时间

    def __str__(self):
        return str(self.uid)


class Weibo(models.Model):
    wid = models.AutoField('微博唯一id', primary_key=True)    # 微博唯一id
    uid = models.ForeignKey(User, verbose_name='发表者用户id',
                            on_delete=models.CASCADE)  # 发表者用户id 外键
    text = models.TextField('微博内容', max_length=140)     # 微博内容
    time = models.DateTimeField(
        '发布时间', auto_now_add=True)                 # 发布时间
    # 微博状态 0：正常 1：仅自己可见 2：系统隐藏
    wtype = models.IntegerField('微博状态', default=0)
    view = models.IntegerField('阅读量', default=0)         # 阅读量
    like = models.IntegerField('点赞数', default=0)         # 点赞数
    comments = models.IntegerField('评论数', default=0)     # 评论数
    is_del = models.BooleanField('是否删除', default=False)  # 是否删除

    def __str__(self):
        return str(self.wid)

    def was_published_recently(self):
        return self.time >= timezone.now() - datetime.timedelta(days=1)


class Comment(models.Model):
    cid = models.AutoField('评论唯一id', primary_key=True)     # 评论唯一id
    wid = models.ForeignKey(Weibo, verbose_name='被评论微博唯一id',
                            on_delete=models.CASCADE)  # 被评论微博唯一id
    uid = models.ForeignKey(User, verbose_name='评论者用户id',
                            on_delete=models.CASCADE)       # 评论者用户id 外键
    text = models.TextField('微博内容', max_length=140)       # 微博内容
    time = models.DateTimeField(
        '评论时间', auto_now_add=True)                   # 评论时间
    like = models.IntegerField('点赞数', default=0)           # 点赞数
    is_del = models.BooleanField('是否删除', default=False)   # 是否删除

    def __str__(self):
        return self.text
