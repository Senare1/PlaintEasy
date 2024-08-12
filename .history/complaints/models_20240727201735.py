from django.db import models
from accounts.constants import CATEGORY
from accounts.models import CommonUser

class Complaint(models.Model):
    category = models.CharField(max_length=64,choices=CATEGORY)
    complainant = models.ForeignKey(CommonUser,on_delete=models.CASCADE)
