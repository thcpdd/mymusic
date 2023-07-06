from django.urls import path
from .views import CommentView

app_name = 'comment'
urlpatterns = [
    path('<int:song_id>', CommentView.as_view(), name='comment')
]
