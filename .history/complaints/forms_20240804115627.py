from django import forms
from .models import Complaint,Proof

class ComplaintForm(forms.ModelForm):
    motif = forms.CharField(
        widget=forms.TimeInput(
            attrs={'placehoder' : 'Motif plainte' ,'class':'form-control','id': 'id_motif'}
        )
    )
    incident_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'placehoder' : 'Motif plainte' ,'class':'form-control','id': 'id_incident_date'}
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'placehoder' : 'Motif plainte' ,'class':'form-control','rows':2,'id': 'id_description'}
        )
    )
    class Meta:
        model = Complaint
        fields = ['motif', 'incident_date', 'description']
    
class ProofForm(forms.ModelForm):
    image = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'image plainte' ,'class':'form-control','id': 'id_image'}
        )
    )
    audio = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'audio plainte' ,'class':'form-control','id': 'id_audio'}
        )
    )
    video = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'video plainte' ,'class':'form-control','id': 'id_video'}
        )
    )
    file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'placehoder' : 'document plainte' ,'class':'form-control','id': 'id_file'}
        )
    )
    class Meta:
        model = Proof
        fields = ['image', 'video', 'audio', 'file']


    