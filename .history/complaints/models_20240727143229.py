from django.db import models
from accounts.constants import CATEGORY


class Complaint(models.Model):
    category = models.CharField(max_length=64,choices=CATEGORY)
