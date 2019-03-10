from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect



urlpatterns=[

    url('^$',views.index, name='index'),
    url(r'^login/$',views.login,name ='login'),
    url(r'^logout/$',views.index,{'next_page': 'accounts:login'}, name='logout'),

]
