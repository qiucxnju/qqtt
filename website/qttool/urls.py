from django.urls import re_path
from . import views
urlpatterns=[
    re_path('words', views.words),
    re_path('^$', views.index),
]
