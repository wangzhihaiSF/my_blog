from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from userprofile.forms import UserLoginForm, UserRegisterForm, ProfileForm
from userprofile.models import Profile


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


@login_required(login_url="userprofile/login/")
def user_delete(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        # 验证删除用户和登录用户是否一致
        if request.user == user:
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            HttpResponse("你没有删除权限")
    else:
        HttpResponse("只接受POST请求")


@login_required(login_url='/userprofile/login/')
def profile_edit(request, user_id):
    user = User.objects.get(id=user_id)
    # user_id 是 OneToOneField 自动生成的字段
    profile = Profile.objects.get(user_id=user_id)

    if request.method == "POST":
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息")

        profile_form = ProfileForm(data=request.POST)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd["phone"]
            profile.avatar = profile_cd["avatar"]
            profile.bio = profile_cd["bio"]
            profile.save()
            return redirect("userprofile:edit", user_id=user_id)
        else:
            return HttpResponse("注册表单信息有误，请重新输入")
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, "profile":profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")
