from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from .constants import STATUT


class CommonManager(BaseUserManager):
    def create_user(self,email,phone,password=None,**extra_fields):
        if email:
            email=self.normalize_email(email)
        user=self.model(email=email,phone=phone,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,phone,password=None,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone, password=password, **extra_fields)

class CommonUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True,blank=True,null=True)
    employee_register = models.CharField(max_length=8,blank=True,null=True)
    status = models.CharField(max_length=16,choices=STATUT,default='CLIENT')
    associer_register = models.CharField(max_length=8,blank=True,null=True)

    object = CommonManager()

    USERNAME_FIELDS = 'email'

    REQUIRED_FIELDS = ['email','phone']

    class Meta:
        pass
    
    def __str__(self):
        return f"{last_name}{first_name}"
    

