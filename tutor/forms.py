from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm


class ClientRegistrationForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['name', 'email', 'image']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


