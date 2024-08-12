from django.shortcuts import render
from .forms import ComplaintForm,ProofForm
from .models import Complaint,Proof

def home(request):
    return render(request,"complaints/index.html")

def help(request):
    return render(request,'complaints/help.html')

def detail(request):
    return render(request,'complaints/detail.html')

def proof_data(request):
    if request.method == 'POST':
        
        if form_proof.is_valid():
            request.session['proof_data'] = form_proof.cleaned_data
    else:
        form_proof=ProofForm()
    return render(request,'complaints/formulaire.html',{})

def let_plaint(request):
    if request.method=='POST':
        form = ComplaintForm(request.POST)
        form_proof = ProofForm(request.POST,request.File)
        if form.is_valid() and form_proof.is_valid():
            motif = form.clean['motif']
            incident_date = form.clean['incident_date']
            description = form.clean['description']
            user = request.user
            complaint = Complaint(
                incident_date=incident_date,
                description=description,
                complainant=user,
                motif=motif
            )
            complaint.save()
            proof_data = request.session.get('proof_data')
            image = form_proof.cleaned_data['image']
            audio = form_proof.cleaned_data['audio']
            video = form_proof.cleaned_data['video']
            file = form_proof.cleaned_data['file']
            complaint = Complaint.objects.all().last()
            proof = Proof(
                image=image,
                audio=audio,
                video=video,
                file=file
            )
            proof.save()
    else:
        form = ComplaintForm()
        form_proof = ProofForm()
    return render(request,'complaints/formulaire.html',{'form': form,'form_proof': form_proof})

def my_plaints(request):
    return render(request,'complaints/my_plaints.html')