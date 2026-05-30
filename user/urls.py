
from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register,name="register"),
    path('sign-in', views.signIn, name="signIn"),
    path('logout', views.sign_out, name="signOut"),
]