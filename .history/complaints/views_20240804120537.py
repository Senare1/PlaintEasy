from django.shortcuts import render
from .forms import ComplaintForm,ProofForm
from .models import Complaint,Proof
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View



@method_decorator(login_required, name='dispatch')
class ComplaintView(View):
    template_name = 'complaints/forms.html'

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

            return redirect('home')  

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


def my_plaints(request):
    return render(request,'complaints/my_plaints.html')