import uuid
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import *
from .db import *


def gen(code, result):
    return {'code': code, 'result': result}

# 接口_评论点赞


def cm_like(request):
    if request.method == "POST":
        cid = request.POST['cid']
        code, result = db_cm_like(cid)
    else:
        code = 403
        result = 'error'
    return JsonResponse(data=gen(code, result))

# 接口_点赞


def wb_like(request):
    if request.method == "POST":
        wid = request.POST['wid']
        code, result = db_wb_like(wid)
    else:
        code = 403
        result = 'error'
    return JsonResponse(data=gen(code, result))

# 接口_发布


def wb_publish(request):
    code = 403
    result = 'error'
    try:
        if request.method == "POST":
            uid = request.session.get('uid')
            text = request.POST['text']
            is_private = request.POST['is_private']
            code, result = db_wb_publish(uid, text, is_private)
    except:
        pass

    return JsonResponse(data=gen(code, result))

# 接口_回复


def cm_publish(request):
    code = 403
    result = 'error'
    try:
        if request.method == "POST":
            uid = request.session.get('uid')
            wid = request.POST['wid']
            text = request.POST['text']
            code, result = db_cm_publish(uid, wid, text)
    except:
        pass

    return JsonResponse(data=gen(code, result))

# 接口_删除微博


def wb_del(request):
    code = 403
    result = 'error'
    try:
        if request.method == "POST":
            uid = request.session.get('uid')
            wid = request.POST['wid']
            code, result = db_wb_del(uid, wid)
    except:
        pass

    return JsonResponse(data=gen(code, result))

# 接口_删除微博


def cm_del(request):
    code = 403
    result = 'error'
    try:
        if request.method == "POST":
            uid = request.session.get('uid')
            wid = request.POST['wid']
            cid = request.POST['cid']
            code, result = db_comment_del(uid, wid, cid)
    except:
        pass

    return JsonResponse(data=gen(code, result))

# 接口_注册


def user_reg(request):
    if request.method == "POST":
        uin = request.POST['uin']
        pwd = request.POST['pwd']
        nick = request.POST['nick']
        email = request.POST['email']
        code, result = db_user_reg(uin, pwd, nick, email)
    else:
        code = 403
        result = 'error'
    return JsonResponse(data=gen(code, result))

# 接口_登录


def user_login(request):
    if request.method == "POST":
        uin = request.POST['uin']
        pwd = request.POST['pwd']
        code, result, user = db_user_login(uin, pwd)
        if code == 200:
            request.session['uid'] = user.uid
            request.session['login'] = True
            request.session.set_expiry(0)
    else:
        code = 403
        result = 'error'
    return JsonResponse(data=gen(code, result))

# 接口_修改信息


def user_modify(request):
    if request.method == "POST":
        uid = request.session.get('uid')
        field = request.POST['field']
        value = request.POST['value']
        try:
            old_pwd = request.POST['old_pwd']
        except:
            old_pwd = ''
        code, result = db_user_modify(uid, field, value, old_pwd)
    else:
        code = 403
        result = 'error'
    return JsonResponse(data=gen(code, result))


def user_logout(request):
    request.session['uid'] = -1
    request.session['login'] = False
    request.session.set_expiry(0)


def user_forgetpwd(request):
    code = 403
    result = 'error'
    if request.method == "POST":
        try:
            step = request.POST['step']
            if step == '1':
                uin = request.POST['uin']
                email = request.POST['email']
                code, result = db_user_forgetpwd_step1(uin, email)
                if code == 200:
                    # 设置凭证
                    result = str(uuid.uuid4())
                    request.session['token_'] = result
                    request.session['uin_'] = uin
                    request.session.set_expiry(0)

            elif step == '2':
                uin_ = request.session.get('uin_')
                token_ = request.session.get('token_')
                uin = request.POST['uin']
                pwd = request.POST['pwd']
                token = request.POST['token']
                # 凭证有误
                if uin != uin_ or token != token_:
                    result = '请从正确入口提交'
                else:
                    code, result = db_user_forgetpwd_step2(uin, pwd)
                    if code == 200:
                        # 销毁凭证
                        request.session['token_'] = str(uuid.uuid4())
                        request.session['uid_'] = str(uuid.uuid4())
                        request.session.set_expiry(0)

        except:
            pass
    return JsonResponse(data=gen(code, result))

# 上传文件


def upload_file(request):
    code = 403
    result = 'error'
    if request.method == "POST":
        print("FILES:", request.FILES)
        uid = request.session.get('uid')
        file = request.FILES.get('avatar', None)
        if file is None:
            code = 201
            result = '未选择文件'
        else:
            fname = file.name
            ext = fname.rsplit('.')[-1]
            # 生成一个uuid作为文件名
            fileName = str(uuid.uuid4()) + "." + ext
            with open(r"%s/%s" % (settings.UPLOAD_ROOT, fileName), 'wb+') as f:
                # 分块写入文件;
                for chunk in file.chunks():
                    f.write(chunk)
            code = 200
            path = "/static/public/upload/"+fileName
            code, result = db_user_modify(uid, 'avatar', path)
    return JsonResponse(data=gen(code, result))
