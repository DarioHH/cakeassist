from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('create_order/', views.CreateOrder.as_view(), name='create_order')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
