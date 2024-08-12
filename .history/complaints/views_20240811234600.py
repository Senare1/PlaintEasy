from django.shortcuts import render,redirect
from .forms import ComplaintForm,ProofForm
from .models import Complaint,Proof,Response
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    complainant = request.user
    number_response = complainant.responses_complaints.all().count()
    context = {
        'number': number_response
    }
    return render(request,"complaints/home.html",context)

def response(request):
    complainant = request.user
    number_response = complainant.responses_complaints.all().count()
    responses = complainant.responses_complaints.all()
    context = {
        'responses': responses,
        'number': number_response
    }   
    return render(request,"complaints/response.html",context)

@login_required
def help(request):
    complainant = request.user
    number_response = complainant.responses_complaints.all().count()
    context = {
        'number': number_response
    }
    return render(request,'complaints/help.html',context)

@login_required
def plaint_detail(request,id):
    complainant = request.user
    number_response = complainant.responses_complaints.all().count()
    complaint = Complaint.objects.get(id=id)
    proofs = complaint.proofs.all()
    context = {
        'complaint': complaint,
        'proofs': proofs,
        'number': number_response,
        }
    return render(request,'complaints/plaint_detail.html',context)

@login_required
def delete_response(request,id):
    response = Response.objects.get(id=id)
    response.delete()
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect('response')

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
            form.add_error(None,'Non autorises')
    else:
        form = ComplaintForm()
    complainant = request.user
    number_response = complainant.responses_complaints.all().count()
    context = {
        'form': form,
        'number': number_response,
    }
    return render(request,'complaints/formulaire.html',context)


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
    complainant = request.user
    number_response = complainant.responses_complaints.all().count()
    context = {
        'form': form,
        'number': number_response,
    }
    return render(request,'complaints/preuves.html',context)


            