from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Clienti

class CustomUserCreationForm(ModelForm):
    class Meta:
        model = Clienti
        fields = '__all__'