from django.shortcuts import render
from django.views import View
from ..index.models import *
from django.contrib.auth.mixins import LoginRequiredMixin  # 登录验证
from django.http import StreamingHttpResponse  # 流下载


class SongPlayView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, song_id):
        hot_search = SongDynamic.objects.select_related('song').order_by('-search').all()[:4]
        song_info = SongInfo.objects.get(id=song_id)
        # 根据歌曲类型获取相关歌曲
        relevant = SongInfo.objects.filter(type=song_info.type)
        # 从会话中获取当前播放列表
        play_list = request.session.get('play_list', [])
        # 判断当前歌曲是否在播放列表中
        if song_info.id not in map(lambda x: x['id'], play_list):
            play_list.append({'id': song_info.id, 'name': song_info.name, 'singer': song_info.singer})
        # 将修改好的播放列表添加至session中
        request.session['play_list'] = play_list
        # 获取歌曲歌词
        lyrics = ''
        if song_info.lyrics != '暂无歌词':
            try:
                with open(f'{song_info.lyrics.url[1:]}', 'r', encoding='utf-8') as f:
                    lyrics = f.read()
            except FileNotFoundError:
                pass
        # 添加歌曲播放次数
        song = SongDynamic.objects.filter(song_id=song_id).first()
        plays = song.plays + 1 if song else 1  # 表中查询不到数据会报错，因此加if
        SongDynamic.objects.update_or_create(song_id=song_id, defaults={'plays': plays})
        # 组织上下文
        context = {
            'hot_search': hot_search,
            'song_info': song_info,
            'relevant': relevant,
            'play_list': play_list,
            'lyrics': lyrics
        }
        return render(request, 'play.html', context)


class SongDownloadView(View):
    def get(self, request, song_id):
        # 添加下载次数
        current_song = SongDynamic.objects.filter(song_id=song_id).first()
        download = current_song.download + 1 if current_song else 1
        SongDynamic.objects.update_or_create(song_id=song_id, defaults={'download': download})
        # 获取歌曲文件路径
        song = SongInfo.objects.get(id=song_id)
        file = song.file.url[1:]
        # 返回给客户端的文件名
        filename = file.split('/')[-1]
        # 固定写法
        response = StreamingHttpResponse(self.file_generator(file))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename={filename}'

        return response

    @staticmethod
    def file_generator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                if f.read(chunk_size):
                    yield f.read(chunk_size)
                else:
                    break
