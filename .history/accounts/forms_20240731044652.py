from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .constants import STATUT
from .models import CommonUser

class SignupForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'exp: Valian Harouna','class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'exp: 76112245','name':'phone','class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'exp: clarisovle14@gmail.com','name':'email','class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=STATUT,
        required=True,
        help_text="Votre status",
        widget=forms.Select(attrs={'placeholder': 'Status','class': 'form-control'})
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control'})
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm','class': 'form-control'})
    )

    class Meta:
        model = CommonUser
        fields = ('full_name', 'phone', 'email', 'status','password1', 'password2')



class LoginForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Mot de passe'
            }
        )
    )

    def get_user(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user

    class Meta:
        model = CommonUser
        fields = ['email','password']

"""
class ProviderForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nom','class':'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Prenom','class':'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Telephone','name':'phone','class':'form-control'})
    )
    provider_register = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Matricule du fournisseur','name':'phone','class':'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email','name':'email','class':'form-control'})
    )
    status = forms.ChoiceField(
        choices=STATUT,
        required=True,
        help_text="Votre status",
        widget=forms.Select(attrs={'placeholder': 'Status','class':'form-control'})
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirm",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm','class':'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','customer_register', 'phone', 'email', 'password1', 'password2')

class EmployeeForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nom','class':'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Prenom','class':'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Telephone','name':'phone','class':'form-control'})
    )
    employee_register = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Matricule employé','name':'phone','class':'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email','name':'email','class':'form-control'})
    )
    status = forms.ChoiceField(
        choices=STATUT,
        required=True,
        help_text="Votre status",
        widget=forms.Select(attrs={'placeholder': 'Status','class':'form-control'})
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password','class':'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirm",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm','class':'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','employee_register', 'phone', 'email', 'password1', 'password2')
"""