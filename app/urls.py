from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),
    path(r'order_detail/(?P<pk>[0-9]+)/$', views.OrderDetailView.as_view(), name='order_detail'),
    path(r'your_order/', views.listYourOrders.as_view(), name='your_order')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
