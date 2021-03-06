"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views, ajax, auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('qtblog.urls')),
    path('file/', include('qtfile.urls')),
    path('findpapa/', include('qtfindpapa.urls')),
    path('tool/', include('qttool.urls')),
    path('member', views.member),
    path('contact', views.contact),
    path('ajax/sendMail', ajax.sendMail),
    path('ajax/markDown', ajax.markDown),
    path('ajax/loadTags', ajax.loadTags),
    path('', views.index),
    path('login', auth.login_view),
    path('logout', auth.logout_view),
    path('register', auth.register),
]
