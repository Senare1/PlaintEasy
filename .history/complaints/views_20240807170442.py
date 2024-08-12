from django.shortcuts import render,redirect
from .forms import ComplaintForm,ProofForm
from .models import Complaint,Proof,Response
from django.contrib.auth.decorators import login_required


def home(request):
    complainant = request.user
    number_response = complainant.responses_complaints.all().count()
    return render(request,"complaints/home.html",{'number': number_response})

def help(request):
    return render(request,'complaints/help.html')

def detail(request):
    return render(request,'complaints/detail.html')


def my_plaints(request):
    complainant = request.user
    number_response = complainant.responses_complaints.all().count()
    plaints = complainant.complaints.all()
    context = {
        'number': number_response,
        'complaints': plaints,

    }
    return render(request,"complaints/etat.html",context)


def let_plaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.complainant = request.user
            form.save()
            return redirect('proof_data')
        else:
            print(form.errors)
    else:
        form = ComplaintForm()
    return render(request,'complaints/formulaire.html',{'form': form})

def proof_data(request):
    if request.method == 'POST':
        form = ProofForm(request.POST,request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            complaint = Complaint.objects.all().filter(complainant=request.user).last()
            form.proof_complaint = complaint
            form.save()
            return redirect('home')
    else:
        form = ProofForm()
    return render(request,'complaints/preuves.html',{'form': form})
            