from django import forms

class ComplaintForm(forms.ModelForm):
    pass

class LoginEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder':'Email','class':'border rounded pill'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'border rounded pill'})
    )

class LoginPhoneForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Email','class':'border rounded pill'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'border rounded pill'})
    )

    