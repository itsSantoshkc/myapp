# cart/views.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import models
from product.models import ProductVariant
from cart.models import Cart, CartItem


@login_required
@require_POST
def add_to_cart(request):
    print('POST data:', request.POST)
    # NAvigate to the product id 
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    next_url = request.POST.get('next', 'home')

    variant = get_object_or_404(ProductVariant, id=variant_id)

    if variant.inventory.quantity < quantity:
        messages.error(request, 'Not enough stock.')
        return redirect(next_url)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, variant=variant)

    if not created:
        item.quantity += quantity
        item.save()

    messages.success(request, f'"{variant.product.name}" added to cart.')
    return redirect(next_url)


def remove_from_cart(request):
    return


def view_cart(request):
    return

def update_cart(request):
    return 