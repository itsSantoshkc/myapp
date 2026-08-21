# cart/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('place-order/', views.place_order, name='place_order'),
    path('order/<uuid:pk>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
]