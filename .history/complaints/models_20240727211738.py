from django.db import models
from accounts.constants import CATEGORY
from accounts.models import CommonUser
from cities_light.models import City,Region,Country

class Location(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE,verbose_name='Pays')
    region = models.ForeignKey(Region,on_delete=models.CASCADE,verbose_name='Region')
    city = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name='Ville')

    class Meta:
        verbose_name = 'Lieu'

    def __str__(self):
        return f"{self.country} {self.region} {self.city}"

class Complaint(models.Model):
    category = models.CharField(max_length=64,choices=CATEGORY,verbose_name="Catégorie")
    complainant = models.ForeignKey(CommonUser,on_delete=models.CASCADE,verbose_name='Plaignant')
    location_incident = models.ForeignKey(Location,on_delete=models.CASCADE,verbose_name="Lieu d'incident",blank=True,null=True)


    class Meta:
        verbose_name = "Plainte"

    def __str__(self):
        return 
