from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # 与user 构建一对一关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    avatar = models.ImageField(upload_to="avatar/%Y%m%d", blank=True)
    # 简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return "user {}".format(self.user.username)


# 信号接收函数，每当新建User 实例时自动调用
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 信号接收函数，每当更新User 实例时自动调用
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


