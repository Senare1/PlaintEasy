from django.shortcuts import render

def home(request):
    return render(request,"complaints/home.html")

def help(request):
    return render(request,'complaints/help.html')

def detail(request):
    return render(request,'complaints/detail.html')
