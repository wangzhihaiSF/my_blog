from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from userprofile.forms import UserLoginForm, UserRegisterForm


def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # form.cleaned_data 将表单的返回值格式化为 dict
            data = user_login_form.cleaned_data
            print(data)
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data["username"], password=data["password"])
            if user:
                login(request, user)
                return redirect("article:article_list")
            else:
                HttpResponse("账户名密码输入错误，请重新输入")
        else:
            HttpResponse("账号密码输入不合法")
    elif request.method == "GET":
        user_login_form = UserLoginForm()
        content = {"form": user_login_form}
        return render(request, "userprofile/login.html", content)
    else:
        HttpResponse("请使用get 或 post 请求")


def user_logout(request):
    logout(request)
    return redirect("article:article_list")


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

