from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Dish(models.Model):
    name = models.CharField(max_length=100, blank=False)
    image = models.CharField(max_length=200, blank=False)
    price = models.IntegerField(default=0, validators=[MinValueValidator(1)], blank=False)
    enabled = models.BooleanField(default=True, blank=False)
    def __str__(self):
        return self.name


class Categori(models.Model):
    name = models.CharField(max_length=100, blank=False)
    dishes = models.ManyToManyField(Dish)
    def __str__(self):
        return self.name