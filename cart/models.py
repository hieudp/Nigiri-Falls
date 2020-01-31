from django.db import models
from django.contrib.auth.models import User

from home.models import Dish

class OrderItem(models.Model):
    amount = models.IntegerField(default=1)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    restaurant = models.CharField(max_length=20, default="Trondheim")
    datetime = models.DateTimeField()
    items = models.ManyToManyField(OrderItem)
    price = models.IntegerField(default=0)
