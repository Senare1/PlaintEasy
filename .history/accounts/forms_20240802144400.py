from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .constants import STATUT
from .models import CommonUser
from django.contrib.auth import authenticate

class SignupForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={'id': 'id_full_name','placeholder': 'exp: Valian Harouna','class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'id': 'id_phone','placeholder': 'exp: 76112245','name':'phone','class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'id': 'id_email','placeholder': 'exp: clarisovle14@gmail.com','name':'email','class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=STATUT,
        required=True,
        help_text="Votre status",
        widget=forms.Select(attrs={'id': 'id_status','placeholder': 'Status','class': 'form-control'})
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'id_password1','placeholder': 'Password','class': 'form-control'})
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'id_password2','placeholder': 'Confirm','class': 'form-control'})
    )

    class Meta:
        model = CommonUser
        fields = ('full_name', 'phone', 'email', 'status','password1', 'password2')

class VerifyForm():
    pass


"""class LoginForm(forms.ModelForm):
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
class LoginEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder':'Email','class':'border p-2 rounded pill'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'border p-2 rounded pill'})
    )

class LoginPhoneForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Email','class':'border p-2 rounded pill'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'border p-2 rounded pill'})
    )

