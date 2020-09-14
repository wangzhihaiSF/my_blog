import markdown
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from article.forms import ArticlePostForm
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


def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单中
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


def article_delete(request, article_id):
    article = ArticlePost.objects.get(id=article_id)
    article.delete()
    return redirect("article:article_list")


def article_safe_delete(request, article_id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")




