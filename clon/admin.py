from django.contrib import admin
# from django.contrib.auth.models import User
from .models import Image,tags, Profile, Review, NewsLetterRecipients, Like

admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(Review)

