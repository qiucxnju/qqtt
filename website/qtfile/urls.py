from django.urls import re_path
from . import views
urlpatterns=[
    re_path('^upload$', views.upload),
    re_path('^$', views.list),
    re_path('^', views.download),
]
