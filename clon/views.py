from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import url,include
from django.contrib.auth import authenticate, login, logout
from .email import send_welcome_email
from django.conf.urls.static import static
from django.contrib.auth.models import User
from . import models
from annoying.decorators import ajax_request
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Image,Location,tags, Profile, Review, NewsLetterRecipients, Like
from django.http  import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import NewImageForm, UpdatebioForm, ReviewForm,PostForm


#Login page view function
def login(request):
    username = 'not logged in'
   
    if request.method == 'POST':
      MyLoginForm = LoginForm(request.POST)
      
      if MyLoginForm.is_valid():
         username = MyLoginForm.cleaned_data['username']
         request.session['username'] = username
      else:
         MyLoginForm = LoginForm()
			
    return render(request, 'registration/login.html')    
    
#Home page view function
@login_required(login_url='/accounts/login/')
def index(request):
    all_images = Image.objects.all()
    all_users = Profile.objects.all()
    next = request.GET.get('next')
    if next: return redirect(next)
    return render(request, 'internal/home.html',  {"all_images": all_images}, {"all_users":all_users})
#Explore page view function
@login_required(login_url='/accounts/login/')
def explore(request):
    return render(request, 'internal/explore.html')

#Profile page view function
@login_required(login_url='/accounts/login/')
def profile(request):
    return render(request, 'internal/userprofile.html')


@login_required(login_url='/accounts/login/')
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

#Log-Out page view function
def logout(request):
    return render(request, 'registration/logout.html')

@login_required(login_url='/accounts/login/')
def home_images(request):
    # Display all images here:

    # images = Image.objects.all()

    locations = Location.objects.all()

    if request.GET.get('location'):
        pictures = Image.filter_by_location(request.GET.get('location'))
    elif request.GET.get('tags'):
        pictures = Image.filter_by_tag(request.GET.get('tags'))
    elif request.GET.get('search_term'):
        pictures = Image.search_image(request.GET.get('search_term'))
    else:
        pictures = Image.objects.all()
    form = PostForm

    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = PostRecipients(name=name, email=email)
            recipient.save()
            send_welcome_email(name, email)

            HttpResponseRedirect('home_images')

    return render(request, 'internal/home.html', {'locations':locations,'tags': tags,'pictures':pictures, 'letterForm':form})

def image(request, id):

    try:
        image = Image.objects.get(pk = id)

    except DoesNotExist:
        raise Http404()

    current_user = request.user
    comments = Review.get_comment(Review, id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']

            review = Review()
            review.image = image
            review.user = current_user
            review.comment = comment
            review.save()

    else:
        form = ReviewForm()



    return render(request, 'image.html', {"image": image, 'form':form,  'comments':comments,
                                          })

@login_required(login_url='/accounts/login/')
def newimage(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('home')

    else:
        form = NewImageForm()
    return render(request, 'internal/upload.html', {"form": form})

# Viewing a single picture

def user_list(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'users.html', context)


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UpdatebioForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('homePage')

    else:
        form = UpdatebioForm()
    return render(request, 'internal/edit_profile.html', {"form": form})

@login_required(login_url='/accounts/login/')
def individual_profile_page(request, username=None):
    if not username:
        username = request.user.username
    # images by user id
    images = Image.objects.filter(user_id=username)

    return render (request, 'internal/user_image_list.html', {'images':images, 'username': username})

def search_users(request):

    # search for a user by their username
    if 'user' in request.GET and request.GET["user"]:
        search_term = request.GET.get("user")
        searched_users = Profile.search_users(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "profiles": searched_users})

    else:
        message = "You haven't searched for any person"
        return render(request, 'search.html', {"message": message})


@login_required(login_url='/accounts/login/')


@login_required(login_url='/accounts/login/')
def individual_profile_page(request, username):
    print(username)
    if not username:
        username = request.user.username
    # images by user id
    images = Image.objects.filter(user_id=username)
    user = request.user
    profile = Profile.objects.get(user=user)
    userf = User.objects.get(pk=username)
    if userf:
        print('user found')
        profile = Profile.objects.get(user=userf)
    else:
        print('No suchuser')


    return render (request, 'registration/userprofile.html', {'images':images, 'profile':profile, 'user':user, 'username': username})


