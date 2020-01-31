from django.db import models
from django.contrib.auth.models import User

"""tar inn et Rating-objekt bestående av en bruker og ratingen denne brukeren har gitt til databasen"""
class Rating(models.Model):
    customer=models.ForeignKey(User, models.CASCADE, default=1)
    rate=models.FloatField(null=True, blank=True)

 