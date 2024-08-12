from django.shortcuts import render,redirect
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
            if user:
                form.add_errors('email','Un utilisateur avec ces identifiants existent déjà')
            if password1 != password2:
                form.add_errors('password2','Les mots ne correspondent pas')
            CommonUser.create_user(email=email,phone=phone,status=status,password=password1,full_name=full_name)
            return redirect('login')

def log_in(request):
    if request.method =='POST':
        form = LoginForm(request.POST)


def forgot(request):
    pass
