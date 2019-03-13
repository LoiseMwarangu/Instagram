from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^$',views.login,name='login'),
    url(r'^search/$', views.search_users, name='search_users'),
    url(r'^image/(\d+)$',views.image,name ='image'),
    url(r'^users/$', views.user_list, name = 'user_list'),
    url(r'^upload$', views.newimage, name='new_image'),
    url(r'^edit$', views.edit_profile, name='edit_profile'),

    url(r'^profile/(?P<username>[0-9]+)$', views.individual_profile_page, name='individual_profile_page'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)