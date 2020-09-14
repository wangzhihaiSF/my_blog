from django.urls import path

from article import views

app_name = "article"

urlpatterns = [
    path("article-list", views.article_list, name="article_list"),
]
