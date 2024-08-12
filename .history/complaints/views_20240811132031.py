from django.shortcuts import render,redirect
from .forms import ComplaintForm,ProofForm
from .models import Complaint,Proof,Response
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    complainant = request.user
    number_response = complainant.responses_complaints.all().count()
    responses = complainant.responses_complaints.all()
    context = {
        'responses': responses,
        'number': number_response
    }
    return render(request,"complaints/home.html",context)

def response(request):
    responses = complainant.responses_complaints.all()
    context = {
        'responses': responses,
    }    
    return render(request,"complaints/home.html",context)

@login_required
def help(request):
    return render(request,'complaints/help.html')

@login_required
def plaint_detail(request,id):
    complaint = Complaint.objects.get(id=id)
    proofs = complaint.proofs.all()
    context = {
        'complaint': complaint,
        'proofs': proofs,
        }
    return render(request,'complaints/plaint_detail.html',context)


@login_required
def my_plaints(request):
    complainant = request.user
    number_response = complainant.responses_complaints.all().count()
    plaints = complainant.complaints.all()
    context = {
        'number': number_response,
        'complaints': plaints,

    }
    return render(request,"complaints/etat.html",context)


@login_required
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


@login_required
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


            