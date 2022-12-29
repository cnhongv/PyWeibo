from django.urls import path
from django.conf import settings
from django.views import static
from django.urls import re_path


from . import views
from . import api
app_name = 'public'

urlpatterns = [
    # 首页
    path('', views.index, name='index'),
    path('<int:page>/', views.index, name='index'),

    # 登录注册
    path('login', views.login, name='login'),
    path('reg', views.reg, name='reg'),
    # 用户注册
    path('logout', views.logout, name='logout'),
    path('setting', views.setting, name='setting'),
    # 找回密码
    path('forgetpwd', views.forgetpwd, name='forgetpwd'),

    path('setting/<str:field>', views.modify_info, name='modify_info'),


    # 发布
    path('publish', views.publish, name='publish'),
    # 发布api
    path('api/publish/', api.wb_publish, name='wb_publish'),

    # ex: /u/5/
    path('u/<int:uid>/', views.profile, name='profile'),
    # ex: /u/5/
    path('u/<int:uid>/<int:page>', views.profile, name='profile'),
    # ex: /detail/5/
    path('detail/<int:wid>/', views.detail, name='detail'),

    # 用户注册
    path('api/reg/', api.user_reg, name='user_reg'),
    # 用户登录
    path('api/login/', api.user_login, name='user_login'),
    # 用户修改资料
    path('api/user_modify/', api.user_modify, name='user_modify'),
    # 忘记密码
    path('api/user_forgetpwd/', api.user_forgetpwd, name='user_forgetpwd'),


    # 点赞
    path('api/wb_like/', api.wb_like, name='wb_like'),
    # 删除
    path('api/wb_del/', api.wb_del, name='wb_del'),
    # 删除评论
    path('api/cm_del/', api.cm_del, name='cm_del'),
    # 上传文件
    path('api/upload_file/', api.upload_file, name='upload_file'),


    # 点赞评论 ex: /api/cm_like/
    path('api/cm_like/', api.cm_like, name='cm_like'),
    # 发评论 ex: /api/cm_publish/
    path('api/cm_publish/', api.cm_publish, name='cm_publish'),

]

if not settings.DEBUG:
    root = settings.STATIC_ROOT
    urlpatterns += [
        re_path('static/(?P<path>.*)$', static.serve, {"document_root": root})
    ]
