from django.shortcuts import render
from django.views import View
from ..index.models import *


class RankingView(View):
    @staticmethod
    def get(request):
        # 搜索框下的热搜歌曲
        hot_search = SongDynamic.objects.select_related('song').order_by('-search').all()[:4]
        # 所有歌曲分类
        labels = SongsSort.objects.all()
        # 查询歌曲排行
        r_type = request.GET.get('type')  # 获取url后的参数
        if r_type:
            dynamics = SongDynamic.objects.select_related('song').filter(song__label=r_type).order_by('-plays')[:10]
        else:
            dynamics = SongDynamic.objects.select_related('song').order_by('-plays')[:10]
        # 组织上下文
        context = {
            'hot_search': hot_search,
            'labels': labels,
            'dynamics': dynamics
        }

        return render(request, 'ranking.html', context)
