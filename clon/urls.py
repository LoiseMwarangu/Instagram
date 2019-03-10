from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect



urlpatterns=[

    path('',views.index, name='index'),
]
