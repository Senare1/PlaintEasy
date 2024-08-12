from django.shortcuts import render

def home(request):
    return render(request,"complaints/index.html")

def help(request):
    return render(request,'complaints/help.html')

def detail(request):
    return render(request,'complaints/detail.html')

def let_plaint(request):
    return render(request,'complaints/formulaire.html')