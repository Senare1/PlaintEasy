from django.shortcuts import render
from .forms import ComplaintForm,ProofForm

def home(request):
    return render(request,"complaints/index.html")

def help(request):
    return render(request,'complaints/help.html')

def detail(request):
    return render(request,'complaints/detail.html')

def let_plaint(request):
    if request.method=='POST':
        form = ComplaintForm(request.POST)
    return render(request,'complaints/formulaire.html')

def my_plaints(request):
    return render(request,'complaints/my_plaints.html')