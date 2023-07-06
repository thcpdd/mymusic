"""MyMusic URL Configuration

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
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from apps.index.views import page_not_found, page_error

urlpatterns = [
    path('', include('apps.index.urls', namespace='index')),  # 首页
    path('user/', include('apps.user.urls', namespace='user')),  # 用户主页
    path('search/', include('apps.search.urls', namespace='search')),  # 搜索功能
    path('ranking.html', include('apps.ranking.urls', namespace='ranking')),  # 歌曲排名
    path('play/', include('apps.play.urls', namespace='play')),  # 歌曲播放页
    path('comment/', include('apps.comment.urls', namespace='comment')),  # 评论页
    # 定义静态资源的路由信息
    # path("static/<path:path>)", serve, {"document_root": settings.STATIC_ROOT}, name="static"),
    # 定义媒体资源的路由信息
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}, name="media"),
    path("admin/", admin.site.urls),
]

# 定义404或500页面必须在settings里面将debug改为False，并且添加允许访问的主机
# DEBUG = False  ALLOWED_HOSTS = ['*']
handler404 = page_not_found
handler500 = page_error
