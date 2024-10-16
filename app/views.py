from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context = {}
    return HttpResponse("WELCOME")
