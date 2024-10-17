from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import AuthUser

class CustomUserCreationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
