from django import forms
from .models import *
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ('image_caption', 'image', 'tag_someone',)

class SignUpForm(forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ['bio','profile_pic','profile_avatar','date']


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment_post'].widget=forms.TextInput()
        self.fields['comment_post'].widget.attrs['placeholder']='comment...'

    class Meta:
        model = Comments
        fields = ('comment_post',)