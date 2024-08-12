from django.shortcuts import render
from .forms import LoginForm,SignupForm
from models import CommonUser

def SignupForm(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            password1=form.clean_data['password1']
            password2=form.clean_data['password2']
            email=form.clean_data['email']
            user = CommonUser.object.get(email=email)

def log_in(request):
    if request.method =='POST':
        form = LoginForm(request.POST)


def forgot(request):
    pass
