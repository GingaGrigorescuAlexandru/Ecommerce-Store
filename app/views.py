from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm

def home(request):
    context = {}
    return render(request, 'app/home.html', context)


def register(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration!")


    context = {'form': form}
    return render(request, 'app/register.html', context)

def loginUser(request):
    form = AuthenticationForm

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get( "username" ).lower()
        password = request.POST.get( "password" )

    try:
        user = User.objects.get(username=username)
    except:
        messages.error(request, "User doesn't exist!")

    user = authenticate(request, username = username, password = password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        messages.error(request, "Username OR password does no exist!")

    context = {}
    return render(request, 'app/login.html', context)
