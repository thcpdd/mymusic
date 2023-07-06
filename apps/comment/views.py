import time
from django.shortcuts import render, redirect, reverse
from django.views import View
from ..index.models import *
from django.core.paginator import Paginator, EmptyPage


class CommentView(View):
    @staticmethod
    def get(request, song_id):
        hot_search = SongDynamic.objects.select_related('song').order_by('-plays').all()[:4]
        song_info = SongInfo.objects.get(id=song_id)
        comments = Comment.objects.filter(song_id=song_id)
        page = request.GET.get('page', 1)
        paginator = Paginator(comments, 5)
        try:
            pages = paginator.page(page)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        context = {
            'hot_search': hot_search,
            'song_info': song_info,
            'pages': pages
        }
        return render(request, 'comment.html', context)

    @staticmethod
    def post(request, song_id):
        comment_text = request.POST.get('comment', '')
        user = request.user.username
        now = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        if comment_text:  # 如果有输入，那么添加评论
            new_comment = Comment()
            new_comment.user = user
            new_comment.text = comment_text
            new_comment.song_id = song_id
            new_comment.date = now
            new_comment.save()
        return redirect(reverse('comment:comment', kwargs={'song_id': song_id}))
