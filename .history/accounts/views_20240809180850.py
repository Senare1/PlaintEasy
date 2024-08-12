from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from .forms import LoginEmailForm,LoginPhoneForm,SignupForm,VerifyForm,ActionForm,ReceiveEmail,ChangePasswordForm
from .models import CommonUser
from complaints.models import Complaint,Response
import random            
from datetime import datetime, timedelta
from django.core.mail import send_mail


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            code = random.randint(100000, 999999)
            expiration_time = datetime.now() + timedelta(minutes=3)
            request.session['verification_code'] = code
            request.session['code_expiration'] = expiration_time.isoformat()
            request.session['user_data'] = form.cleaned_data

            if CommonUser.objects.filter(email=email).exists():
                form.add_error('email', 'Cet email est déjà utilisé.')
            elif CommonUser.objects.filter(phone=phone).exists():
                form.add_error('phone', 'Ce numéro de téléphone est déjà utilisé.')

            send_mail(
                'Votre code de vérification',
                f'Voici votre code de vérification, svp ne le communiquez à personne : {code}',
                'arsenenikiema685@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('verify_email')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})



def verify_email(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            expiration_time = datetime.fromisoformat(request.session.get('code_expiration'))
            
            if datetime.now() > expiration_time:
                form.add_error('code', 'Le code de vérification a expiré.')
            elif code == request.session.get('verification_code'):
                user_data = request.session.get('user_data')
                if CommonUser.objects.filter(email=user_data['email']).exists():
                    form.add_error(None, 'Cet email est déjà utilisé.')
                elif CommonUser.objects.filter(phone=user_data['phone']).exists():
                    form.add_error(None, 'Ce numéro de téléphone est déjà utilisé.')
                else:
                    user = CommonUser.objects.create_user(
                        email=user_data['email'],
                        phone=user_data['phone'],
                        password=user_data['password1'],
                        full_name=user_data['full_name'],
                        address=user_data['address'],
                        status=user_data['status'],
                    )
                    del request.session['verification_code']
                    del request.session['user_data']
                    del request.session['code_expiration']
                    return redirect('login_email')
            else:
                form.add_error('code', 'Code de vérification incorrect.')
    else:
        form = VerifyForm()

    return render(request, 'accounts/verify_email.html', {'form': form})


def regenerate_verification_code(request):
    if 'user_data' in request.session:
        user_data = request.session['user_data']
        verification_code = random.randint(100000, 999999)
        expiration_time = datetime.now() + timedelta(minutes=3)
        request.session['verification_code'] = verification_code
        request.session['code_expiration'] = expiration_time.isoformat()

        send_mail(
            'Votre nouveau code de vérification',
            f'Voici votre nouveau code de vérification, svp ne le communiquez à personne : {verification_code}',
            'arsenenikiema685@gmail.com',
            [user_data['email']],
            fail_silently=False,
        )
        return redirect('verify_email')
    else:
        return redirect('signup')


def dashboard(request):
    nb_total = Complaint.objects.all().count()
    nb_treated = Complaint.objects.filter(status="treated").count()
    nb_rejected = Complaint.objects.filter(status="rejected").count()
    nb_running = nb_total - nb_rejected -nb_treated
    complaints = Complaint.objects.all()[:5]
    context = {
        "nb_total" : nb_total,
        "nb_treated" : nb_treated,
        "nb_rejected" : nb_rejected,
        "nb_running" : nb_running,
        'complaints' : complaints,
    }
    return render(request,'accounts/dashboard.html',context)

def users(request):
    nb_total = CommonUser.objects.all().exclude(is_staff=True,is_superuser=True).count()
    nb_customer = CommonUser.objects.filter(status="CLIENT").exclude(is_staff=True,is_superuser=True).count()
    nb_citizen = CommonUser.objects.filter(status="CITOYEN").exclude(is_staff=True,is_superuser=True).count()
    users = CommonUser.objects.all().exclude(is_staff=True,is_superuser=True)[:5]
    context = {
        "nb_total" : nb_total,
        "nb_customer" : nb_customer,
        "nb_citizen" : nb_citizen,
        "users" : users,
    }
    return render(request,'accounts/users.html',context)

def all_users(request):
    users = CommonUser.objects.all().exclude(is_staff=True,is_superuser=True)
    context = {
        "users" : users,
    }
    return render(request,'accounts/all_users.html',context)

def all_citozens(request):
    users = CommonUser.objects.filter(status="CITOYEN").exclude(is_staff=True,is_superuser=True)
    context = {
        "users" : users,
    }
    return render(request,'accounts/all_citozens.html',context)

def all_customers(request):
    users = CommonUser.objects.filter(status="CLIENT").exclude(is_staff=True,is_superuser=True)
    context = {
        "users" : users,
    }
    return render(request,'accounts/all_customers.html',context)

def delete(request,email):
    user = CommonUser.objects.get(email=email)
    previous_page = request.META.get('HTTP_REFERER')
    if user:
        user.delete()
        return redirect(previous_page)
    else:
        return redirect('users')


def statistics(request):
    total_complaints = Complaint.objects.count()
    treated_complaints = Complaint.objects.filter(status='treated').count()
    rejected_complaints = Complaint.objects.filter(status='rejected').count()
    in_progress_complaints = total_complaints - treated_complaints -rejected_complaints
    
    context = {
        'total_complaints': total_complaints,
        'treated_complaints': treated_complaints,
        'rejected_complaints': rejected_complaints,
        'in_progress_complaints': in_progress_complaints,
    }
    return render(request, 'accounts/statistics.html', context)



def receiving(request):
    total_complaints = Complaint.objects.all().count()
    receiving_complaints = Complaint.objects.all()
    context = {
        'receiving_complaints': receiving_complaints,
        "total_complaints" : total_complaints,
    }
    return render(request,'accounts/receiving.html',context)

def give_message(user,msg):
    if msg == "rejected":
        msg = f"Salut M(r) {user} nous vous envoyons ce message pour vous informer et vous presenter nos sincères excuses que votre plainte a ete rejete pour des raisons non fondee.Merci de nous comprendre et de nous revenir avec des amples preuves"
    elif msg == "treated":
        msg = f"Salut M(r) {user} ,votre plainte vient d'etre traitee avec succès.Contacter ces numeros pour une conclusion fine.Merci à bientot"
    elif msg == "running":
        msg = f"Salut M(r) {user} ,nous accusons reception de votre plainte.Nous vous reviendrons.Merci à bientot"    
    return msg

def complaint_detail(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    complainant = complaint.complainant.full_name
    proofs = complaint.proofs.all()
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            reject = form.cleaned_data['reject']
            if status:
                complaint.status = "treated"
                response = Response(
                    complainant=complaint.complainant,
                    complaint=complaint,
                    message=give_message(complaint.complainant,msg="treated")
                )
                response.save()
                send_mail(
                    'Votre plainte a bien ete traite',
                    f"{give_message(complaint.complainant,msg="treated")}",
                    'arsenenikiema685@gmail.com',
                    [complaint.complainant.email],
                    fail_silently=False,
                )
            elif reject:
                complaint.status = "rejected"
                response = Response(
                    complainant=complaint.complainant,
                    complaint=complaint,
                    message=give_message(complaint.complainant,msg="rejected")
                )
                response.save()

                send_mail(
                    'Votre plainte a ete rejete',
                    f"{give_message(complaint.complainant,msg="rejected")}",
                    'arsenenikiema685@gmail.com',
                    [complaint.complainant.email],
                    fail_silently=False,
                )
            else:
                send_mail(
                    'Votre plainte a ete rejete',
                    f"{give_message(complaint.complainant,msg="running")}",
                    'arsenenikiema685@gmail.com',
                    [complaint.complainant.email],
                    fail_silently=False,
                )
            
            previous_page = request.META.get('HTTP_REFERER')
            if previous_page:
                return redirect(previous_page)
            else:
                return redirect('receiving')
    else: 
        form = ActionForm()
    context = {
        'complaint': complaint,
        'complainant': complainant,
        'form': form,
        'proofs': proofs,
    }

    return render(request, 'accounts/complaint_detail.html', context)
    
        
def rejection(request):
    rejected_complaints = Complaint.objects.all().filter(status="rejected")
    context = {
        "rejected_complaints" : rejected_complaints,
    }
    return render(request,'accounts/rejection.html',context)


def treated(request):
    treated_complaints = Complaint.objects.all().filter(status="treated")
    context = {
        "treated_complaints" : treated_complaints,
    }
    return render(request,'accounts/treated.html',context)

def running(request):
    running_complaints = Complaint.objects.all().filter(status="running")
    context = {
        "running_complaints" : running_complaints,
    }
    return render(request,'accounts/running.html',context)

def log_out(request):
    logout(request)
    return redirect('login_email')


def chat(request):
    return render(request,'accounts/chat.html')

def signup_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            status = form.cleaned_data['status']
            phone = form.cleaned_data['phone']
            full_name = form.cleaned_data['full_name']
            address = form.cleaned_data['address']
            if CommonUser.objects.filter(email=email,phone=phone,status=status).exists():
                form.add_error(None,f"Un {status} avec ses identifiants existe")
            elif (password1 != password2 ):
                form.add_error('password1',f"Identifiants invalides")
            else:
                user = CommonUser.objects.create_user(
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    status=status,
                    address=address,
                    password=password1
                )
                return redirect ('all_users')
    else:
        form = SignupForm()
    return render(request,'accounts/signup_user.html',{'form': form })

def forgot(request):
    pass


def login_email(request):
    if request.method == "POST":
        form = LoginEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('dashboard')
                else:
                    return redirect('home')
            else:
                form.add_error(None, "Identifiants invalides")
    else:
        form = LoginEmailForm()
    return render(request, 'accounts/login_email.html', {'form': form})


def login_phone(request):
    if request.method == "POST":
        form = LoginPhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request, username=phone, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Identifiants invalides")
    else:
        form = LoginPhoneForm()
    return render(request, 'accounts/login_phone.html', {'form': form})


def user_detail(request,id):
    user = CommonUser.objects.get(id=id)
    return render(request,'accounts/user_detail.html',{'user': user})

def forgot(request):
    if request.method == 'POST':
        form = ReceiveEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if email is not None:
                user = CommonUser.objects.get(email=email)
                if user:
                    code = random.randint(100000, 999999)
                    expiration_time = datetime.now() + timedelta(minutes=3)
                    request.session['verification_code'] = code
                    request.session['code_expiration'] = expiration_time.isoformat()
                    request.session['email'] = email
                    request.session['user_data'] = form.cleaned_data
                    send_mail(
                        'Confirmer votre identité',
                        f'Voici votre code de confirmation, svp ne le communiquez à personne : {code}',
                        'arsenenikiema685@gmail.com',
                        [email],
                        fail_silently=False,
                    )
                    return redirect('verify_code')
                else:
                    form.add_error('email','Compte non trouvé')
    else:
        form = ReceiveEmail()
    return render(request,'accounts/forgot.html',{'form':form})


def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            expiration_time = datetime.fromisoformat(request.session.get('code_expiration'))
            
            if datetime.now() > expiration_time:
                form.add_error('code', 'Le code de vérification a expiré.')
            elif code == request.session.get('verification_code'):
                user_data = request.session.get('user_data')
                if CommonUser.objects.filter(email=user_data['email']).exists():
                    email = user_data['email']
                    return redirect('change_password')
                else:
                    del request.session['verification_code']
                    del request.session['user_data']
                    del request.session['code_expiration']
                    return redirect('login_email')
            else:
                form.add_error('code', 'Code de vérification incorrect.')
    else:
        form = VerifyForm()

    return render(request, 'accounts/verify_code.html', {'form': form})


def regenerate_email_code(request):
    if 'user_data' in request.session:
        user_data = request.session['user_data']
        verification_code = random.randint(100000, 999999)
        expiration_time = datetime.now() + timedelta(minutes=3)
        request.session['verification_code'] = verification_code
        request.session['code_expiration'] = expiration_time.isoformat()

        send_mail(
                'Confirmer votre identité',
                f'Voici votre code de confirmation, svp ne le communiquez à personne : {code}',
                'arsenenikiema685@gmail.com',
                [email],
                fail_silently=False,
            )
        return redirect('verify_email')
    else:
        return redirect('signup')


def change_password(request,email):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = CommonUser.objects.get(email=email)
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                user.password = password1
            else:
                form.add_error(None,'Mot de passe ne correspondent pas')
    else:
        form = ChangePasswordForm()
    return render(request,'accounts/mot_de_passe.html',{'form':form})
 