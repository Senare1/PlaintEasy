from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from .constants import STATUT

class CommonManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Un mail est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone, password=password, **extra_fields)

class CommonUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r"^\+?1?\d{8,8}$")
    full_name = models.CharField(max_length=32)
    phone = models.CharField(validators=[phone_regex], max_length=16, unique=True, verbose_name="Telephone", blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    status = models.CharField(max_length=16, choices=STATUT, default='CLIENT')
    
    objects = CommonManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = "Utilisateur"
    
    def __str__(self):
        return f"{self.full_name}"
