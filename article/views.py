import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from article.forms import ArticlePostForm
from article.models import ArticlePost


def article_list(request):
    search = request.GET.get("search")
    order = request.GET.get("order")
    if search:
        if order == "total_views":
            article_all = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by("-total_views")
        else:
            article_all = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by("-total_views")
    else:
        search = ""
        if order == "total_views":
            article_all = ArticlePost.objects.all().order_by("-total_views")
        else:
            article_all = ArticlePost.objects.all()

    # 每页显示 1 篇文章
    paginator = Paginator(article_all, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles_page = paginator.get_page(page)

    context = {'articles_page': articles_page, "order": order, "search": search}
    return render(request, 'article/list.html', context)


def article_detail(request, article_id):
    article = ArticlePost.objects.get(id=article_id)
    # 浏览量 +1
    if request.user != article.author:
        article.total_views += 1
        article.save(update_fields=['total_views'])

    md = markdown.Markdown(extensions=[
        "markdown.extensions.extra",
        "markdown.extensions.codehilite",
        "markdown.extensions.toc", ])
    article.body = md.convert(article.body)
    # 新增了md.toc对象
    context = {'article': article, 'toc': md.toc}
    return render(request, "article/detail.html", context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    # user = User.objects.get(id=article_id)
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单中
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
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


@login_required(login_url="/userprofile/login/")
def article_delete(request, article_id):
    article = ArticlePost.objects.get(id=article_id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    article.delete()
    return redirect("article:article_list")


@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, article_id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=article_id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无删除这篇文章。")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/userprofile/login/')
def article_update(request, article_id):
    article = ArticlePost.objects.get(id=article_id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
