from django.urls import path

from . import views

urlpatterns = [
    path('checkout/esewa/success/', views.esewa_success, name='esewa_success'),
    path('checkout/esewa/failure/', views.esewa_failure, name='esewa_failure'),
]
