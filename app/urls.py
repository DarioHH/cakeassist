from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('create_order/', views.create_order, name='create_order')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
