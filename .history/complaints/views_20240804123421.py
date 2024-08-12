from django.shortcuts import render
from .forms import ComplaintForm,ProofForm
from .models import Complaint,Proof


def home(request):
    return render(request,"complaints/index.html")

def help(request):
    return render(request,'complaints/help.html')

def detail(request):
    return render(request,'complaints/detail.html')


def my_plaints(request):
    return render(request,'complaints/my_plaints.html')

def let_plaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.complainant = request.user
            form.save()
            return redirect('home')
    else:
        form = ComplaintForm()
    return render(request,'complaints/formulaire.html',{'form': form})

def proof_data(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST,request.FILES)
        if form.is_valid():
            form.proof_complaint = request.user
            form.save()
            return redirect('home')
    else:
        form = ComplaintForm()
    return render(request,'complaints/formulaire.html',{'form': form})
            