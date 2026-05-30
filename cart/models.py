# cart/models.py
from django.db import models
from django.conf import settings
import product
from product.models import Product, ProductVariant


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    variants = models.ManyToManyField(ProductVariant, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cart.user} — {self.product.name} x{self.quantity}'


    @property
    def line_total(self):
        return self.quantity * self.product.base_price