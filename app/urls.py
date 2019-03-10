from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('create_order', views.create_order, name='create_order')
]

