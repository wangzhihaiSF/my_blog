from django.contrib import admin

# Register your models here.
from article.models import ArticlePost

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)

