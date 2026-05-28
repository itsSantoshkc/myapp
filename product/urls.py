
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('product/<int:id>/', views.productDetails, name="productDetails"),
    path('search/', views.searchProduct, name="searchProduct"),
]