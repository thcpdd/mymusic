from django.shortcuts import render, redirect, reverse
from django.views import View
from ..index.models import *
from django.db.models import Q, F
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class SearchView(View):
    @staticmethod
    def get(request, page):
        # 获取会话中的内容
        keyword = request.session.get('keyword')
        if keyword:  # 搜索框有内容
            songs = SongInfo.objects.filter(Q(name__icontains=keyword) | Q(singer=keyword)).order_by('-release')\
                .all()
        else:  # 搜索框无内容
            songs = SongInfo.objects.order_by('-release').all()[:20]

        paginator = Paginator(songs, 10)  # 一页10个数据
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:  # page不是整型
            pages = paginator.page(1)
        except EmptyPage:  # 传入的page参数超出分页列表范围
            pages = paginator.page(paginator.num_pages)  # 返回所有页面的最后一页
        # 添加歌曲搜索次数
        if keyword:
            results = SongInfo.objects.filter(name__icontains=keyword).all()
            for result in results:
                dynamic = SongDynamic.objects.filter(song_id=result.id)  # 查询该数据是否在动态表中
                if dynamic:  # 表中有数据则增加搜索次数
                    dynamic.update(search=F('search') + 1)
                else:  # 表中无数据则新增一条记录
                    new_dynamic = SongDynamic(search=1, download=0, plays=0, song_id=result.id)
                    new_dynamic.save()
        hot_search = SongDynamic.objects.select_related('song').order_by('-search').all()[:4]
        # 组织上下文
        context = {
            'hot_search': hot_search,
            'pages': pages
        }
        return render(request, 'search.html', context)

    @staticmethod
    def post(request, page):
        request.session['keyword'] = request.POST.get('kword')  # 获取搜索框中的内容
        return redirect(reverse('search:search', kwargs={'page': page}))
