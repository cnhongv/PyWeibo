from math import ceil
from django.conf import settings
import hashlib
from django.db.models import F, Q
from .models import *


def gen(code, result):
    # 生成返回的对象格式
    return {'code': code, 'result': result}


def md5(data_string):
    # 存储密码需要
    obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


def db_wb_list(start=0, end=5):
    # 数据库__读取微博列表
    try:
        result = Weibo.objects.filter(
            is_del=False, wtype=0).order_by('-time')[start:end]
        pages = ceil(len(Weibo.objects.filter(is_del=False, wtype=0)) / 5) - 1
        code = 200
    except Weibo.DoesNotExist:
        code = 404
        result = 'not found'
    return code, result, pages


def db_wb_detail(uid, wid):
    # 数据库__读取微博详情
    comments = ''
    try:
        weibo = Weibo.objects.get(wid=wid, is_del=False)
        # 他人查看私密博客
        if weibo.uid.uid != uid and weibo.wtype > 0:
            weibo = 'private'
        try:
            comments = Comment.objects.filter(
                wid=weibo, is_del=False).order_by('-time')
        except:
            pass
        code = 200
    except Weibo.DoesNotExist:
        code = 404
        weibo = 'not found'
    return code, weibo, comments


def db_wb_profile(uid, owner, start=0, end=5):
    # 数据库__个人主页
    pages = 0
    try:
        user = User.objects.get(uid=uid)
    except User.DoesNotExist:
        code = 404
        result = 'user not found'
        return code, result, pages
    try:
        if owner:
            result = Weibo.objects.filter(
                Q(wtype=0) | Q(wtype=1),
                uid=user,
                is_del=False).order_by('-time')[start:end]
            pages = int(len(Weibo.objects.filter(
                Q(wtype=0) | Q(wtype=1),
                uid=user,
                is_del=False)) / 5)
        else:
            result = Weibo.objects.filter(
                uid=user,
                is_del=False, wtype=0).order_by('-time')[start:end]
            pages = int(len(Weibo.objects.filter(
                uid=user,
                is_del=False, wtype=0)) / 5)

        code = 200
    except Weibo.DoesNotExist:
        code = 404
        result = 'not found'
    return code, result, pages


def db_wb_view(wid):
    # 数据库__读取微博的阅读量
    try:
        Weibo.objects.filter(wid=wid).update(view=F('view') + 1)
        code = 200
        result = 'success'
    except Weibo.DoesNotExist:
        code = 404
        result = 'not found'
    return code, result


def db_cm_like(cid):
    # 数据库__增加评论的点赞量
    try:
        Comment.objects.filter(cid=cid).update(like=F('like') + 1)
        code = 200
        result = 'success'
    except Comment.DoesNotExist:
        code = 404
        result = 'not found'
    return code, result


def db_wb_like(wid):
    # 数据库__增加微博的点赞量
    try:
        Weibo.objects.filter(wid=wid).update(like=F('like') + 1)
        code = 200
        result = 'success'
    except Weibo.DoesNotExist:
        code = 404
        result = 'not found'
    return code, result


def db_wb_publish(uid, text, is_private):
    # 数据库__发布微博
    try:
        if len(text) > 140 or len(text) == 0:
            code = 201
            result = '微博要在140字以内哦~'
            return code, result
        user = User.objects.get(uid=uid)
        if is_private == 'false':
            wtype = 0
        elif is_private == 'true':
            wtype = 1
        else:
            wtype = 2
        Weibo.objects.create(uid=user, text=text, wtype=wtype)
        code = 200
        result = 'success'
    except:
        code = 500
        result = 'publish err'
    return code, result


def db_cm_publish(uid, wid, text):
    # 数据库__发布评论
    try:
        if len(text) > 140 or len(text) == 0:
            code = 201
            result = '评论要在140字以内哦~'
            return code, result
        try:
            user = User.objects.get(uid=uid)
        except:
            code = 202
            result = '请先登录~'
            return code, result
        try:
            weibo = Weibo.objects.get(wid=wid)
        except:
            code = 404
            result = '要评论的微博不存在~'
            return code, result
        Comment.objects.create(uid=user, wid=weibo, text=text)
        Weibo.objects.filter(wid=wid).update(comments=F('comments') + 1)
        code = 200
        result = 'success'
    except:
        code = 500
        result = 'publish err'
    return code, result


def db_wb_wtype(wid, wtype=1):
    # 数据库__隐藏微博
    try:
        Weibo.objects.filter(wid=wid).update(wtype=wtype)
        code = 200
        result = 'success'
    except Weibo.DoesNotExist:
        code = 404
        result = 'not found'
    return code, result


def db_wb_del(uid, wid):
    # 数据库__删除微博
    try:
        Weibo.objects.filter(uid=uid, wid=wid).update(is_del=True)
        code = 200
        result = 'success'
    except Weibo.DoesNotExist:
        code = 404
        result = 'not found'
    return code, result


def db_comment_del(uid, wid, cid):
    # 数据库__删除评论
    code = 200
    result = 'success'
    try:
        weibo = Weibo.objects.get(wid=wid)
        owner = weibo.uid.uid == uid
        if owner:
            Comment.objects.filter(cid=cid).update(is_del=True)
            Weibo.objects.filter(wid=wid).update(comments=F('comments') - 1)
        else:
            cm = Comment.objects.get(cid=cid)
            if cm.uid.uid != uid:
                code = 403
                result = '您无权限删除该评论'
            else:
                Comment.objects.filter(cid=cid).update(is_del=True)
                Weibo.objects.filter(wid=wid).update(
                    comments=F('comments') - 1)
    except:
        code = 404
        result = 'not found'
    return code, result


def db_user_login(uin, pwd):
    # 数据库__登录
    try:
        user = User.objects.get(uin=uin, pwd=md5(pwd))
        if user.uin == uin:
            code = 200
            result = 'sucess'
            User.objects.filter(uid=user.uid).update(
                last_login=datetime.datetime.now())
            return code, result, user
    except:
        code = 403
        result = '用户名或密码错误'
        user = ''
        return code, result, user


def db_user_forgetpwd_step1(uin, email):
    # 数据库__忘记密码第一步
    code = 403
    result = '用户名不存在/错误或email错误'
    try:
        user = User.objects.get(uin=uin, email=email)
        if user.uin == uin:
            code = 200
            result = 'success'
    except:
        pass

    return code, result


def db_user_forgetpwd_step2(uin, pwd):
    # 数据库__忘记密码第二步
    code = 403
    result = '重置失败'
    try:
        if len(pwd) > 18 or len(pwd) < 6:
            code = 201
            result = '密码应为6-18位字符'
            return code, result
        User.objects.filter(uin=uin).update(pwd=md5(pwd))
        code = 200
        result = 'success'
    except:
        pass
    return code, result


def db_user_modify(uid, field, value, old_pwd=''):
    # 数据库__修改用户信息
    try:
        code = 200
        result = 'success'
        if field == 'nick':
            if len(value) > 20 or len(value) < 2:
                code = 201
                result = '昵称在2-20字之间'
            else:
                try:
                    User.objects.get(nick=value)
                    code = 201
                    result = '昵称被占用'
                except:
                    User.objects.filter(uid=uid).update(nick=value)
        elif field == 'email':
            if len(value) > 32 or len(value) < 3:
                code = 202
                result = '邮箱格式有误'
            else:
                try:
                    User.objects.get(email=value)
                    code = 202
                    result = '邮箱被占用'
                except:
                    User.objects.filter(uid=uid).update(email=value)
        elif field == 'pwd':
            try:
                if len(value) > 18 or len(value) < 6:
                    code = 203
                    result = '密码应为6-18位字符'
                else:
                    if len(User.objects.filter(uid=uid, pwd=md5(old_pwd))) > 0:
                        User.objects.filter(uid=uid, pwd=md5(
                            old_pwd)).update(pwd=md5(value))
                    else:
                        code = 403
                        result = '原密码错误'
            except:
                code = 403
                result = '原密码错误'
        elif field == 'avatar':
            if len(value) > 256:
                code = 204
                result = '头像网址太长，应在256字符以内'
            else:
                User.objects.filter(uid=uid).update(avatar=value)

    except:
        code = 500
        result = '修改失败'
    return code, result


def db_user_reg(uin, pwd, nick, email):
    # 数据库__注册
    try:
        try:
            user = User.objects.get(uin=uin)
            if user.uin == uin:
                code = 201
                result = '用户名已注册，请登录或更换用户名'
                return code, result
        except:
            pass

        try:
            user = User.objects.get(nick=nick)
            if user.nick == nick:
                code = 201
                result = '昵称已占用，请登录或更换昵称'
                return code, result
        except:
            pass

        try:
            user = User.objects.get(email=email)
            if user.email == email:
                code = 201
                result = '邮箱已注册，请登录或更换邮箱'
                return code, result
        except:
            pass

        if len(email) > 32 or len(pwd) < 6:
            code = 201
            result = '邮箱格式有误'
            return code, result

        if len(pwd) > 18 or len(pwd) < 6:
            code = 201
            result = '密码应为6-18位字符'
            return code, result

        User.objects.create(uin=uin, pwd=md5(pwd), nick=nick, email=email)
        code = 200
        result = '注册成功'

    except:
        code = 500
        result = '注册失败'
    return code, result
