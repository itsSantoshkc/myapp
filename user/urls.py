
from django.urls import path

from . import views

urlpatterns = [
    path('auth/register', views.register,name="register"),
    path('auth/sign-in', views.signIn, name="signIn"),
    path('auth/logout', views.sign_out, name="signOut"),
    path('auth/address/add', views.add_address, name="add_address"),
]