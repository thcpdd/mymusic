from django.urls import path
from .views import RankingView

app_name = 'ranking'
urlpatterns = [
    path('', RankingView.as_view(), name='ranking'),
]
