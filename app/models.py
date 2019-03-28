from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from timesheet.models import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    baker = models.BooleanField(null=False, default=False)

    def __unicode__(self):
        return str(self.user)

    def __str__(self):
        return str(self.user)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


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
    
    def __str__(self):
        return "{}  {}  ".format(self.delivery_day_to_str, self.shop)
    
    def __bool__(self):
        return bool(self.items)
    @property
    def delivery_day_to_str(self):
        return self.delivery_day.strftime("%Y-%m-%d")
    
    @property
    def items(self):
        return Item.objects.filter(order=self.pk)
    
    def get_items(self):
       return ' | '.join(['{} []'.format(item.cake, item.quantity) for item in self.items])
    
    def get_absolute_url(self):
        return reversed('order_detail', args=[str(self.id)])

class Item(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

