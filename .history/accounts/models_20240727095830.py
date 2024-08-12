from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password



class CommonManager(BaseUserManager):
    def create_user(self,email,phone,**kwargs):
        pass


    def create_superuser(self,email,phone,**kwargs):
        pass

class CommonUser(AbstractBaseUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True,blank=True,null=True)

    

