from django.contrib import admin

# Register your models here.
from .models import Shop, Size, Cake, Order, Profile

admin.site.register(Shop)
admin.site.register(Size)
admin.site.register(Cake)
admin.site.register(Order)
admin.site.register(Profile)

