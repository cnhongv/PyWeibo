"""MyWeibo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public.urls')),
]


def not_found(request, exception):
    
    # print(settings.STATIC_ROOT)
    context={
        'user_logged_in': request.session.get('login'),
        'uid': request.session.get('uid'),
        'msg': '页面不存在'
    }
    return render(request, 'public/404.html', context)

# 处理404页面
handler404 = not_found
