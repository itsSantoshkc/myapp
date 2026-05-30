# cart/views.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404,render
from django.views.decorators.http import require_POST
from django.db import models
from product.models import ProductVariant
from cart.models import Cart, CartItem


@login_required
@require_POST
def add_to_cart(request):
    quantity = int(request.POST.get('quantity', 1))
    next_url = request.POST.get('next', '/')

    group_labels = request.POST.get('group_labels', '').split(',')
    group_labels = [g.strip() for g in group_labels if g.strip()]

    variant_ids = []
    for label in group_labels:
        variant_id = request.POST.get(label)
        if variant_id:
            variant_ids.append(variant_id)

    if not variant_ids:
        messages.error(request, 'No variant selected.')
        return redirect(next_url)

    variants = ProductVariant.objects.filter(id__in=variant_ids).select_related('product')

    if not variants.exists():
        messages.error(request, 'Invalid variants.')
        return redirect(next_url)

    product = variants.first().product

    for variant in variants:
        if variant.stock < quantity:
            messages.error(request, f'Not enough stock for {variant.type}: {variant.value}.')
            return redirect(next_url)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    # find existing item with same product AND same variants
    variant_ids_set = set(str(v.id) for v in variants)
    existing_item = None

    for item in cart.items.filter(product=product).prefetch_related('variants'):
        item_variant_ids = set(str(v.id) for v in item.variants.all())
        if item_variant_ids == variant_ids_set:
            existing_item = item
            break

    if existing_item:
        existing_item.quantity += quantity
        existing_item.save()
    else:
        new_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity,
        )
        new_item.variants.set(variants)

    messages.success(request, f'"{product.name}" added to cart.')
    return redirect(next_url)

def remove_from_cart(request):
    return

@login_required
def view_cart(request):
    cart = Cart.objects.prefetch_related(
        'items__product__images',
        'items__variants',
    ).filter(user=request.user).first()

    items = []
    total = 0

    if cart:
        for item in cart.items.all():
            line_total = item.line_total
            total += line_total
            items.append({
                'item': item,
                'product': item.product,
                'variants': item.variants.all(),  # .all() on M2M
                'image': item.product.images.filter(is_primary=True).first(),
                'line_total': line_total,
            })


    return render(request, 'cart/cart.html', {
        'items': items,
        'total': total,
        'cart': cart,
    })
def update_cart(request):
    return 