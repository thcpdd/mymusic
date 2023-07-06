from django.shortcuts import render, redirect, reverse
from django.views import View
from .models import MyUser
from django.contrib.auth.mixins import LoginRequiredMixin  # 登录验证
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from ..index.models import *


class LoginView(View):
    @staticmethod
    def get(request):
        return render(request, 'login.html')

    @staticmethod
    def post(request):
        username = request.POST.get('loginUser')
        password = request.POST.get('password')

        if not all([username, password]):
            return render(request, 'login.html', {'tips': '数据不完整'})

        userinfo = authenticate(request, username=username, password=password)  # 从数据库中获取用户信息

        if userinfo:
            login(request, userinfo)
            next_page = request.GET.get('next', reverse('user:user'))
            response = redirect(next_page)
            return response
        else:
            return render(request, 'login.html', {'tips': '用户名不存在或密码错误'})


class RegisterView(View):
    @staticmethod
    def get(request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not all([username, mobile, password1, password2]):
            return render(request, 'register.html', {'tips': '数据不完整'})

        if self.is_chinese(username):
            return render(request, 'register.html', {'tips': '用户名不能包含中文'})

        if password1 != password2:
            return render(request, 'register.html', {'tips': '两次输入密码不一致'})

        try:
            userinfo = MyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            userinfo = None

        if userinfo:
            return render(request, 'register.html', {'tips': "用户名已存在"})

        new_user = MyUser.objects.create_user(username=username, password=password1, mobile=mobile)
        new_user.is_active = 1

        return redirect(reverse('user:login'))

    @staticmethod
    def is_chinese(string):
        """判断用户名是否包含中文"""
        for content in string:
            if u'\u4e00' <= content <= u'\u9fff':
                return True
        return False


class UserHomeView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        hot_search = SongDynamic.objects.select_related('song').order_by('-search').all()[:4]
        context = {
            'hot_search': hot_search
        }
        return render(request, 'home.html', context)


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect(reverse('index:index'))
