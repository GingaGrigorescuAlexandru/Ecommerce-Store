from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import AuthUser, Produse, ProprietatiProduse

class CustomUserCreationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class ProductCreationForm(ModelForm):
    class Meta:
        model = Produse
        fields = '__all__'

class PropertiesProductForm(ModelForm):
    class Meta:
        model = ProprietatiProduse
        fields = '__all__'
        exclude = ["produs"]

