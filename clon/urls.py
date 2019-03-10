from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect



urlpatterns=[
    #homepage
    url('^$',views.index, name='index'),
    #login url
    url(r'^login/$',views.login,name ='login'),
    #logout url
    url(r'^logout/$',views.index,{'next_page': 'accounts:login'}, name='logout'),
    url(r'^explore/$',views.explore,name ='explore'),   
    #Notification url 
    url(r'^notification/$',views.notification,name ='notification'),
    #profile page url 
    url(r'^profile/$',views.profile,name ='profile'),
    #url to upload pictures 
    url(r'^upload/$',views.upload,name ='upload'),

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

