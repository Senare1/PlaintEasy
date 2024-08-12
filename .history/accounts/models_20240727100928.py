from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password



class CommonManager(BaseUserManager):
    def create_user(self,email,phone,password=None,**extra_fields):
        if email:
            email=self.normalize_email(email)
        user=self.model(email=email,phone=phone,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,phone,password=None,**extra_fields):
        pass

class CommonUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True,blank=True,null=True)

    

