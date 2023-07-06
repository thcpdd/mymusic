from django.shortcuts import render
from django.views import View
from .models import *


class IndexView(View):
    @staticmethod
    def get(request):
        song_dynamic = SongDynamic.objects.select_related('song')
        # 热搜歌曲
        hot_search = song_dynamic.order_by('-search').all()[:8]
        # 音乐分类
        labels = SongsSort.objects.all()
        # 热门歌曲
        popular_songs = song_dynamic.order_by('-plays').all()[:10]
        # 新歌推荐
        recommend = SongInfo.objects.order_by('-release').all()[:3]
        # 热门下载
        hot_download = song_dynamic.order_by('-download').all()[:6]
        # 首页底部的热门搜索与热门下载
        tabs = [hot_search[:6], hot_download]
        # 组织上下文
        context = {
            'hot_search': hot_search,
            'labels': labels,
            'popular_songs': popular_songs,
            'recommend': recommend,
            'tabs': tabs
        }
        return render(request, 'index.html', context)


# 定义404页面
def page_not_found(request, exception):
    return render(request, '404.html', status=404)


# 定义500页面
def page_error(request):
    return render(request, "404.html", status=500)
