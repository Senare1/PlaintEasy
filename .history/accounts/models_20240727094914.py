from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class CommonUser(AbstractBaseUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True,blank=True,null=True)

    

