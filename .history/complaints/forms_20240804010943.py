from django import forms
from .models import Complaint,Proof

class ComplaintForm(forms.Form):
    motif = forms.CharField(
        widget=forms.TimeInput(
            attrs={'placehoder' : 'Motif plainte' ,'class':'form-control'}
        )
    )
    date_incident = forms.CharField(
        widget=forms.TimeInput(
            attrs={'placehoder' : 'Motif plainte' ,'class':'form-control'}
        )
    )
    description = forms.CharField(
        widget=forms.TimeInput(
            attrs={'placehoder' : 'Motif plainte' ,'class':'form-control'}
        )
    )
    
class ProofForm(forms.Form):
    image = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'image plainte' ,'class':'form-control'}
        )
    )
    audio = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'audio plainte' ,'class':'form-control'}
        )
    )
    video = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'video plainte' ,'class':'form-control'}
        )
    )
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'document plainte' ,'class':'form-control'}
        )
    )


    