from django.shortcuts import render,redirect
from .forms import LoginForm,SignupForm
from models import CommonUser

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            password1=form.clean_data['password1']
            password2=form.clean_data['password2']
            email=form.clean_data['email']
            user = CommonUser.object.get(email=email)
            if user:
                form.add_errors('email','Un utilisateur avec ces identifiants existent déjà')
            if password1 != password2:
                form.add_errors('password2','Les mots ne correspondent pas')
            CommonUser.create_user(email=email,phone=phone,status=status,password=password1,full_name=full_name)
            return redirect('login')
    else:
        form = LoginForm()
    return render(request,'accounts/signup.html',context={'form':form})

def log_in(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            


def forgot(request):
    pass


def signup(request):
    if request.method == 'POST':
        form = LearnerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('learner_email')
            phone = form.cleaned_data.get('learner_phone')
            code = random.randint(100000, 999999)
            expiration_time = datetime.now() + timedelta(minutes=3)
            request.session['verification_code'] = code
            request.session['code_expiration'] = expiration_time.isoformat()
            request.session['user_data'] = form.cleaned_data

            if CustomUser.objects.filter(learner_email=email).exists():
                form.add_error('email', 'Cet email est déjà utilisé.')
            elif CustomUser.objects.filter(learner_phone=phone).exists():
                form.add_error('phone', 'Ce numéro de téléphone est déjà utilisé.')

            send_mail(
                'Votre code de vérification',
                f'Voici votre code de vérification, svp ne le communiquez à personne : {code}',
                'arsenenikiema685@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('verify_email')  # Utilisez le nom d'URL ici
    else:
        form = LearnerForm()
    return render(request, 'accounts/inscription.html', {'form': form})



def verify_email(request):
    if request.method == 'POST':
        verify_form = VerifyForm(request.POST)
        if verify_form.is_valid():
            code = verify_form.cleaned_data.get('code')
            expiration_time = datetime.fromisoformat(request.session.get('code_expiration'))
            
            if datetime.now() > expiration_time:
                verify_form.add_error('code', 'Le code de vérification a expiré.')
            elif code == request.session.get('verification_code'):
                # Code de vérification correct, vérifier l'existence de l'email et du téléphone
                user_data = request.session.get('user_data')
                if CustomUser.objects.filter(learner_email=user_data['learner_email']).exists():
                    verify_form.add_error(None, 'Cet email est déjà utilisé.')
                elif CustomUser.objects.filter(learner_phone=user_data['learner_phone']).exists():
                    verify_form.add_error(None, 'Ce numéro de téléphone est déjà utilisé.')
                else:
                    # Créer l'utilisateur ici
                    user = CustomUser.objects.create_user(
                        learner_email=user_data['learner_email'],
                        learner_phone=user_data['learner_phone'],
                        password=user_data['password1'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        learner_level=user_data['learner_level'],
                        learner_faculty=user_data['learner_faculty'],
                    )
                    del request.session['verification_code']
                    del request.session['user_data']
                    del request.session['code_expiration']
                    return redirect('login')
            else:
                verify_form.add_error('code', 'Code de vérification incorrect.')
    else:
        verify_form = VerifyForm()

    return render(request, 'accounts/verify_email.html', {'verify_form': verify_form})

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
            [user_data['learner_email']],
            fail_silently=False,
        )
        return redirect('verify_email')  # Utilisez le nom d'URL ici
    else:
        return redirect('signup')  # Utilisez le nom d'URL ici


def learner_login(request):
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
    return render(request, 'accounts/connexion.html', {'form': form, 'error_message': error_message})


