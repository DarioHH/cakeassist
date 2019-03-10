from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=60)
    phone = models.IntegerField
    addres = models.CharField(max_length=60)
    email = models.EmailField()


class Size(models.Model):
    size = models.CharField(max_length=60)

    def __str__(self):
        return self.size.upper()

class Cake(models.Model):
    name = models.CharField(max_length=60)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Order(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


