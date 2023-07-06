from django.urls import path
from .views import SongPlayView, SongDownloadView

app_name = 'play'
urlpatterns = [
    path('<int:song_id>', SongPlayView.as_view(), name='play'),
    path('donwload/<int:song_id>', SongDownloadView.as_view(), name='download')
]
