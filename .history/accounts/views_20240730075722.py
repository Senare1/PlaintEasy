from django.shortcuts import render,redirect
from .forms import LoginForm,SignupForm
from models import CommonUser
from complaints.models import Complaint            


def forgot(request):
    pass


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
        form = LoginForm()
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
                        status=user_data['status'],
                    )
                    del request.session['verification_code']
                    del request.session['user_data']
                    del request.session['code_expiration']
                    return redirect('login')
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


def log_in(request):
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


def dashboard(request):
    nb_traite = Complaint.objects.filter(status="TRAITEE").count()
    nb_rejete = Complaint.objects.filter(status="REJETEE").count()
    nb_running = Complaint.objects.filter(status="EN COURS").count()
    context = {
        "nb_traite" : nb_traite,
        "nb_rejete" : nb_rejete,
        "nb_running" : nb_running,
    }
    return render(request,'accounts/dashboard.html',context)