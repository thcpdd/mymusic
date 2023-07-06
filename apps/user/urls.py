from django.urls import path
from .views import LoginView, UserHomeView, RegisterView, LogoutView

app_name = 'user'
urlpatterns = [
    path('', UserHomeView.as_view(), name='user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register')
]
