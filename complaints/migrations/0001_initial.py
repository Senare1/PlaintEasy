# Generated by Django 5.0.7 on 2024-08-12 06:10

import complaints.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128)),
                ('date_borned', models.DateField()),
                ('status', models.CharField(max_length=128)),
                ('salary', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('Location_borned', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Employer',
            },
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motif', models.CharField(max_length=64, verbose_name='Motif')),
                ('incident_registered', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('treated', 'Plainte traitee'), ('rejected', 'Plainte rejectee'), ('running', 'Plainte en cours de traitement')], default='running', max_length=32)),
                ('incident_date', models.DateField()),
                ('description', models.TextField()),
                ('complainant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to=settings.AUTH_USER_MODEL, verbose_name='Plaignant')),
            ],
            options={
                'verbose_name': 'Plainte',
            },
        ),
        migrations.CreateModel(
            name='Proof',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='complaints/proof/images', validators=[complaints.models.FileValidator(allowed_types=['image/jpeg', 'image/png', 'image/gif', 'image/webp'], message='Seules les images sont autorisées.')], verbose_name='Preuve en image')),
                ('video', models.FileField(blank=True, null=True, upload_to='complaints/proof/videos', validators=[complaints.models.FileValidator(allowed_types=['video/mp4', 'video/avi', 'video/mpeg', 'video/webm', 'video/mkv'], message='Seules les vidéos sont autorisées.')], verbose_name='Preuve en video')),
                ('audio', models.FileField(blank=True, null=True, upload_to='complaints/proof/audios', validators=[complaints.models.FileValidator(allowed_types=['audio/mpeg', 'audio/mp3', 'audio/ogg', 'audio/wav', 'audio/x-wav'], message='Seuls les fichiers audio sont autorisés.')], verbose_name='Preuve en audio')),
                ('document', models.FileField(blank=True, null=True, upload_to='complaints/proof/documents', validators=[complaints.models.FileValidator(allowed_types=['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'], message='Seuls les documents sont autorisés.')], verbose_name='Preuve en fichier')),
                ('proof_complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proofs', to='complaints.complaint')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date_receiving', models.DateField(auto_now_add=True)),
                ('status_deleted', models.BooleanField(default=False)),
                ('complainant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses_complaints', to=settings.AUTH_USER_MODEL)),
                ('complaint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='complaints.complaint')),
            ],
        ),
    ]