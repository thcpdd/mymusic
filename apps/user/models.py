from django.db import models
from django.contrib.auth.models import AbstractUser  # django自带的用户模型类


# 自定义用户模型类
class MyUser(AbstractUser):
    # 在django用户模型类的基础上再次增加用户字段
    qq = models.CharField('QQ号', max_length=15)
    wechat = models.CharField('微信号', max_length=20)
    mobile = models.CharField('手机号', max_length=11, unique=True)

    def __str__(self):
        return self.username
