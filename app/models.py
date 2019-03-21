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
        return "{} - {}".format(self.name, self.size)

class Order(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_day = models.DateField(name='delivery_day')

    class Meta:
        ordering = ['created_at']

    def get_absolute_url(self):
        return reversed('order_detail')

class Item(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

