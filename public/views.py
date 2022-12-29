# Create your views here.
from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
from django.db.models import F
from .models import *
from . import api
from . import db

# 首页
def index(request, page=0):
    code, latest_weibo_list, pages = db.db_wb_list(page*5, (page+1)*5)
    # 阅读量+1
    for wb in latest_weibo_list:
        db.db_wb_view(wb.wid)

    context = {
        'weibo_list': latest_weibo_list,
        'len': len(latest_weibo_list),
        'page': page,
        'pre': page-1,
        'next': page+1,
        'pages': pages,
        'user_logged_in': request.session.get('login'),
        'uid': request.session.get('uid'),
    }
    # print(context)
    # print(len(latest_weibo_list))
    return render(request, 'public/index.html', context)

# 个人主页
def profile(request, uid, page=0):
    try:
        user=User.objects.get(uid=uid)
        owner=request.session.get('uid')==uid
        code, latest_weibo_list,pages = db.db_wb_profile(uid, owner, page*5, (page+1)*5)
        # 阅读量+1
        for wb in latest_weibo_list:
            db.db_wb_view(wb.wid)
        context = {
            'weibo_list': latest_weibo_list,
            'user': user,
            'owner': owner,
            'page': page,
            'pre': page-1,
            'next': page+1,
            'pages': pages,
            'uid': uid,
            'user_logged_in': request.session.get('login')
        }
    except User.DoesNotExist:
        context = {
            'msg': '用户不存在',
            'uid': request.session.get('uid'),
            'user_logged_in': request.session.get('login')
        }
        return render(request, 'public/404.html', context)
    return render(request, 'public/profile.html', context)

# 微博详情
def detail(request, wid):
    uid=request.session.get('uid')
    code, weibo, comments=db.db_wb_detail(uid, wid)
    if code==200:
        db.db_wb_view(wid)
        owner=uid==weibo.uid.uid
    else:
        owner=False
    context={
        'weibo': weibo,
        'comments': comments,
        'uid': uid,
        'owner': owner,
        'user_logged_in': request.session.get('login')
    }  
    return render(request, 'public/detail.html', context)

# 发布
def publish(request):
    if request.session.get('login') != True:
        return login(request)
    context={
        'user_logged_in': request.session.get('login'),
        'uid': request.session.get('uid'),
    }
    return render(request, 'public/publish.html', context)

# 登录
def login(request):
    context={
        'user_logged_in': request.session.get('login'),
        'uid': request.session.get('uid'),
    }
    return render(request, 'public/login.html', context)

# 注册
def reg(request):
    context={
        'user_logged_in': request.session.get('login'),
        'uid': request.session.get('uid'),
    }
    return render(request, 'public/reg.html', context)

# 忘记密码
def forgetpwd(request):
    context={
        'user_logged_in': request.session.get('login'),
        'uid': request.session.get('uid'),
    }
    return render(request, 'public/forgetpwd.html', context)

# 进入设置
def setting(request):
    if request.session.get('login') != True:
        return login(request)
    context={
        'user_logged_in': request.session.get('login'),
        'uid': request.session.get('uid'),
    }
    return render(request, 'public/setting.html', context)

# 修改用户资料
def modify_info(request, field):
    if request.session.get('login') != True:
        return login(request)
    uid=request.session.get('uid')
    context={
        'user_logged_in': request.session.get('login'),
        'uid': uid,
        'user': User.objects.get(uid=uid)
    }
    if field not in ['nick', 'email', 'pwd', 'avatar']:
        context['msg']='设置不存在'
        return render(request, 'public/404.html', context)
    return render(request, 'public/setting/{}.html'.format(field), context)


# 注销登录
def logout(request):
    if request.session.get('login') != True:
        return login(request)
    request.session['uid'] = -1
    request.session['login'] = False
    return redirect('/')

