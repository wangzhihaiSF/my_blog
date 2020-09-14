import markdown
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from article.models import ArticlePost


def article_list(request):
    articles = ArticlePost.objects.all()
    context = {"articles": articles}
    return render(request, 'article/list.html', context)


def article_detail(request, article_id):
    article = ArticlePost.objects.get(id=article_id)
    article.body = markdown.markdown(article.body, extensions=[
        "markdown.extensions.extra",
        "markdown.extensions.codehilite",
    ])
    context = {"article": article}
    return render(request, "article/detail.html", context)
