from django.db import models
from django.contrib.auth.models import User




# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=60)
    phone = models.IntegerField
    addres = models.CharField(max_length=60)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Size(models.Model):
    size = models.CharField(max_length=60)

    def __str__(self):
        return self.size.upper()

class Cake(models.Model):
    name = models.CharField(max_length=60)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    shop = models.ForeignKey(Shop, related_name='orders', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    class Meta:
        ordering = ['created_at']



class Item(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

