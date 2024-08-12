from django.shortcuts import render
from .forms import LoginForm

def signup(request):
    pass

def log_in(request):
    if request.method =='POST':
        form = LoginForm(request.POST)


def forgot(request):
    pass
