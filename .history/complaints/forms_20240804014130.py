from django import forms
from .models import Complaint,Proof

class ComplaintForm(forms.Form):
    motif = forms.CharField(
        widget=forms.TimeInput(
            attrs={'placehoder' : 'Motif plainte' ,'class':'form-control','id': 'id_motif'}
        )
    )
    incident_date = forms.CharField(
        widget=forms.TimeInput(
            attrs={'placehoder' : 'Motif plainte' ,'class':'form-control','id': 'id_incident_date'}
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'placehoder' : 'Motif plainte' ,'class':'form-control','rows':2,'id': 'id_description'}
        )
    )
    
class ProofForm(forms.Form):
    image = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'image plainte' ,'class':'form-control','id': 'id_image'}
        )
    )
    audio = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'audio plainte' ,'class':'form-control','id': 'id_audio'}
        )
    )
    video = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'video plainte' ,'class':'form-control','id': 'id_video'}
        )
    )
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'document plainte' ,'class':'form-control','id': 'id_file'}
        )
    )


    