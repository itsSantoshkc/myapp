# cart/urls.py
from django.urls import path
from cart import views

urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
]