from django.shortcuts import render
from .forms import ComplaintForm,ProofForm

def home(request):
    return render(request,"complaints/index.html")

def help(request):
    return render(request,'complaints/help.html')

def detail(request):
    return render(request,'complaints/detail.html')

def proof_data(request):
    if request.method == 'POST':
        form = ProofForm(request.POST,request.File)
        if form.is_valid():
            request.session['user_data'] = form.cleaned_data
    else:
        form=ProofForm()
    return redirect('let_plaint')

def let_plaint(request):
    if request.method=='POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
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
            image = proof_data['image']
            audio = proof_data['audio']
            video = proof_data['video']
            file = proof_data['file']
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
    return render(request,'complaints/formulaire.html',{'form': 'form'})

def my_plaints(request):
    return render(request,'complaints/my_plaints.html')