from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import LoginEmailForm,LoginPhoneForm,SignupForm,VerifyForm
from .models import CommonUser
from complaints.models import Complaint
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
                # Code de vérification correct, vérifier l'existence de l'email et du téléphone
                user_data = request.session.get('user_data')
                if CommonUser.objects.filter(email=user_data['email']).exists():
                    form.add_error(None, 'Cet email est déjà utilisé.')
                elif CommonUser.objects.filter(phone=user_data['phone']).exists():
                    form.add_error(None, 'Ce numéro de téléphone est déjà utilisé.')
                else:
                    # Créer l'utilisateur ici
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


"""def log_in(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message = "Identifiant(s) invalides"
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})
"""

def dashboard(request):
    nb_total = Complaint.objects.all().count()
    nb_treated = Complaint.objects.filter(status="TRAITEE").count()
    nb_rejected = Complaint.objects.filter(status="REJETEE").count()
    nb_running = Complaint.objects.filter(status="EN COURS").count()
    context = {
        "nb_total" : nb_total,
        "nb_treated" : nb_treated,
        "nb_rejected" : nb_rejected,
        "nb_running" : nb_running,
    }
    return render(request,'accounts/dashboard.html',context)

def users(request):
    nb_total = CommonUser.objects.all().exclude(is_staff=True,is_superuser=True).count()
    nb_customer = CommonUser.objects.filter(status="CLIENT").exclude(is_staff=True,is_superuser=True).count()
    nb_citizen = CommonUser.objects.filter(status="CITOYEN").exclude(is_staff=True,is_superuser=True).count()
    users = CommonUser.objects.all().exclude(is_staff=True,is_superuser=True)
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
    return render(request,'accounts/statistics.html')


def receiving(request):
    return render(request,'accounts/receiving.html')


def rejection(request):
    return render(request,'accounts/rejection.html')


def treated(request):
    return render(request,'accounts/treated.html')

def running(request):
    return render(request,'accounts/running.html')

def log_out(request):
    logout(request.user)
    return redirect('login_email')

def profile(request):
    return render(request,'accounts/profile.html')

def settings(request):
    return render(request,'accounts/settings.html')

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
