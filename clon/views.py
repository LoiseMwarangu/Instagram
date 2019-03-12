from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf.urls import url,include
from django.contrib.auth import authenticate, login, logout
from .forms import PostForm
from .email import send_welcome_email
from django.conf.urls.static import static
from .models import Profile, Image
from django.contrib.auth.models import User
from . import models
from annoying.decorators import ajax_request
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required



#Login page view function
def register(request):
    return render(request, 'registration/registration.html')    
    
#Home page view function
@login_required(login_url='/login/')
def index(request):
    all_images = Image.objects.all()
    all_users = Profile.objects.all()
    next = request.GET.get('next')
    if next: return redirect(next)
    return render(request, 'internal/home.html',  {"all_images": all_images}, {"all_users":all_users})
#Explore page view function
@login_required(login_url='/login/')
def explore(request):
    return render(request, 'internal/explore.html')



#Notification page view function
@login_required(login_url='/login/')
def notification(request):
    return render(request, 'internal/notification.html')

#Profile page view function
@login_required(login_url='/accounts/login/')
def profile(request):
    return render(request, 'internal/userprofile.html')


#Login page view function
@login_required(login_url='/login/')
def upload(request):
    current_user = request.user
    p = Profile.objects.filter(id=current_user.id).first()
    imageuploader_profile = Image.objects.filter(imageuploader_profile=p).all()
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.imageuploader_profile= p
            post.save()
            return redirect('/')
    else:
        form =PostForm
    return render(request, 'internal/upload.html', {"form": form})

# #Log-Out page view function
# def logout(request):
#     return render(request, 'registration/logout.html')


