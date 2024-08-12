from django.contrib import admin
from .models import Proof,Complaint,Employee,Response

admin.site.register(Proof)
admin.site.register(Complaint)
admin.site.register(Employee)
admin.site.register(Response)