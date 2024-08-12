from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class CustomerForm(UserCreationForm):
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
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email','name':'email','class':'form-control'})
    )
    learner_level = forms.ChoiceField(
        choices=LEARNER_LEVEL,
        required=True,
        help_text="Niveau scolaire",
        widget=forms.Select(attrs={'placeholder': 'CLASSE','class':'form-control'})
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
        fields = ('first_name', 'last_name', 'phone', 'email','learner_level', 'password1', 'password2')
