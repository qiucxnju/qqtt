from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import logging

logger = logging.getLogger(__name__)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, username=phone, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else :
            return HttpResponse("登录失败")
    return render(request, 'website/login.html')    

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        firstname = request.POST['firstname']
        if (len(phone) != 11 or not phone.isdigit()):
            return HttpResponse("请输入正确的手机号")
        if (password != password2):
            return HttpResponse("密码输入不一致")
        if (len(password) < 6):
            return HttpResponse("密码小于6位")
        if (len(password) < 6):
            return HttpResponse("密码小于6位")
        if (len(password) < 6):
            return HttpResponse("密码小于6位")
        user = User.objects.create_user(phone, email, password)
        user.first_name = firstname
        user.save()
        logger.error(request.POST)
        logger.error(user)
        login(request, user)
        return HttpResponseRedirect('/')
    return render(request, 'website/register.html')    

