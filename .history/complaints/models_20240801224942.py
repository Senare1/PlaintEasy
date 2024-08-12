from django.db import models
from accounts.constants import CATEGORY,STATUT_COM
from accounts.models import CommonUser
from cities_light.models import City,Region,Country
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import mimetypes
from django.utils.text import slugify


@deconstructible
class FileValidator:
    def __init__(self, allowed_types, message=None):
        self.allowed_types = allowed_types
        self.message = message or 'Type de fichier non autorisé.'

    def __call__(self, value):
        mime_type, encoding = mimetypes.guess_type(value.name)
        if mime_type not in self.allowed_types:
            raise ValidationError(self.message)

validate_image = FileValidator(
    allowed_types=[
        'image/jpeg', 'image/png', 'image/gif', 'image/webp'
    ],
    message='Seules les images sont autorisées.'
)

validate_video = FileValidator(
    allowed_types=[
        'video/mp4', 'video/avi', 'video/mpeg', 'video/webm', 'video/mkv'
    ],
    message='Seules les vidéos sont autorisées.'
)

validate_audio = FileValidator(
    allowed_types=[
        'audio/mpeg', 'audio/mp3', 'audio/ogg', 'audio/wav', 'audio/x-wav'
    ],
    message='Seuls les fichiers audio sont autorisés.'
)

validate_document = FileValidator(
    allowed_types=[
        'application/pdf', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ],
    message='Seuls les documents sont autorisés.'
)


class Complaint(models.Model):
    motif = models.CharField(max_length=64,choices=CATEGORY,verbose_name="Motif")
    complainant = models.ForeignKey(CommonUser,on_delete=models.CASCADE,verbose_name='Plaignant')
    incident_registered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32,choices=STATUT_COM,default="EN COURS")
    incident_day = models.DateField(blank=True,null=True)
    description = models.TextField()


    class Meta:
        verbose_name = "Plainte"

    def __str__(self):
        return f"{self.description | truncatewords:3}"


class Proof(models.Model):
    image = models.FileField(upload_to="complaints/proof/images",validators=[validate_image],blank=True,null=True,verbose_name="Preuve en image")
    video = models.FileField(upload_to="complaints/proof/videos",validators=[validate_video],blank=True,null=True,verbose_name="Preuve en video")
    audio = models.FileField(upload_to="complaints/proof/audios",validators=[validate_audio],blank=True,null=True,verbose_name="Preuve en audio")
    document = models.FileField(upload_to="complaints/proof/documents",validators=[validate_document],blank=True,null=True,verbose_name="Preuve en document")
    proof_complaint = models.ForeignKey(Complaint,on_delete=models.CASCADE,related_name="proofs")

    def __str__(self):
        return self.image.name if self.image else (
            self.video.name if self.video else (
                self.audio.name if self.audio else (
                    self.document.name if self.document else 'No File'
                )
            )
        )