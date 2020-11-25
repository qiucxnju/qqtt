from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return render(request, 'qtblog/index.html')
def blog(request):
    return HttpResponse('发送失败')
# Create your views here.
