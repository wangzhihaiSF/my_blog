from django.urls import path

from article import views

app_name = "article"

urlpatterns = [
    path("article-list", views.article_list, name="article_list"),
    path("article-detail/<int:article_id>/", views.article_detail, name="article_detail"),
    path("article-create/", views.article_create, name="article_create"),
    path("article-delete/<int:article_id>/", views.article_delete, name="article_delete"),
    path('article-safe-delete/<int:article_id>/', views.article_safe_delete, name='article_safe_delete'),
    path('article-update/<int:article_id>/', views.article_update, name='article_update'),
]
