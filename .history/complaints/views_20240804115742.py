from django.shortcuts import render
from .forms import ComplaintForm,ProofForm
from .models import Complaint,Proof

from django.shortcuts import render, redirect
from django.views import View
from .models import Complaint, Proof
from .forms import ComplaintForm, ProofForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class ComplaintView(View):
    template_name = 'complaints/complaint_form.html'

    def get(self, request, *args, **kwargs):
        complaint_form = ComplaintForm()
        proof_form = ProofForm()
        return render(request, self.template_name, {
            'form': complaint_form,
            'form_proof': proof_form
        })

    def post(self, request, *args, **kwargs):
        complaint_form = ComplaintForm(request.POST)
        proof_form = ProofForm(request.POST, request.FILES)

        if complaint_form.is_valid():
            complaint = complaint_form.save(commit=False)
            complaint.complainant = request.user
            complaint.save()

            if proof_form.is_valid():
                proof = proof_form.save(commit=False)
                proof.proof_complaint = complaint
                proof.save()

            return redirect('complaints:success')  

        return render(request, self.template_name, {
            'form': complaint_form,
            'form_proof': proof_form
        })


def home(request):
    return render(request,"complaints/index.html")

def help(request):
    return render(request,'complaints/help.html')

def detail(request):
    return render(request,'complaints/detail.html')


def let_plaint(request):
    if request.method=='POST':
        form = ComplaintForm(request.POST)
        form_proof = ProofForm(request.POST,request.FILES)
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
            return redirect('home')
    else:
        form = ComplaintForm()
        form_proof = ProofForm()
    return render(request,'complaints/formulaire.html',{'form': form,'form_proof': form_proof})

def my_plaints(request):
    return render(request,'complaints/my_plaints.html')