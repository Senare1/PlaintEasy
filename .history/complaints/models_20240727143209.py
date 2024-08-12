from django.db import models

class Complaint(models.Model):
    category = models.CharField(max_length=64,choices=CATEGORY)
