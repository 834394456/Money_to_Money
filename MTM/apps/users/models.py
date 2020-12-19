from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=11,unique=True)
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    # default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
    #                                     on_delete=models.SET_NULL, verbose_name='默认地址')
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name