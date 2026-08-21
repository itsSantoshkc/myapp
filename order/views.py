import uuid

from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from config import settings
from order.models import Order, OrderItem
from payment.views import (
    ESEWA_PRODUCT_CODE,
    ESEWA_SECRET_KEY,
    generate_signature,
)
from user.models import Address


def generate_transaction_uuid():
    return uuid.uuid4().hex[:20].upper()

# Create your views here.
@login_required
@require_POST
def place_order(request):
    print(request.POST)
    address_id = request.POST.get('address_id')
    payment_method = request.POST.get('payment')
    next_url = request.POST.get('next', '/')

    address = get_object_or_404(Address, id=address_id, user=request.user)

    cart = Cart.objects.prefetch_related(
        'items__product',
        'items__variants',
    ).filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.error(request, 'Cart is empty.')
        return redirect('view_cart')

    # calculate totals
    subtotal = sum(item.line_total for item in cart.items.all())
    tax_amount = 0
    delivery_charge = 0
    total_amount = subtotal + tax_amount + delivery_charge

    # create order
    order = Order.objects.create(
        user=request.user,
        address=address,
        payment_method=payment_method,
        subtotal=subtotal,
        tax_amount=tax_amount,
        delivery_charge=delivery_charge,
        total_amount=total_amount,
        status='pending',
        payment_status='unpaid',
    )

    # create order items from cart
    for cart_item in cart.items.all():
        order_item = OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            unit_price=cart_item.product.base_price,
        )
        order_item.variants.set(cart_item.variants.all())

    print("order id",order.id)

    if payment_method == 'esewa':
        order_id = str(order.id)

    # save order id in session to retrieve on callback
        request.session['pending_order_id'] = order_id

        signature = generate_signature(
        total_amount=str(total_amount),
        transaction_uuid=order_id,
        product_code=ESEWA_PRODUCT_CODE,
        secret_key=ESEWA_SECRET_KEY,
    )

        esewa_payload = {
        'amount': str(subtotal),
        'tax_amount': str(tax_amount),
        'total_amount': str(total_amount),
        'transaction_uuid': order_id,
        'product_code': ESEWA_PRODUCT_CODE,
        'product_service_charge': '0',
        'product_delivery_charge': str(delivery_charge),
        'success_url': request.build_absolute_uri('/checkout/esewa/success/'),
        'failure_url': request.build_absolute_uri('/checkout/esewa/failure/'),
        'signed_field_names': 'total_amount,transaction_uuid,product_code',
        'signature': signature,
    }

        return render(request, 'checkout/esewa_redirect.html', {
        'esewa_payload': esewa_payload,
        'esewa_url': 'https://rc-epay.esewa.com.np/api/epay/main/v2/form',
    })

    elif payment_method == 'cod':
        order.payment_status = 'unpaid'
        order.status = 'confirmed'
        order.save()
        cart.items.all().delete()
        messages.success(request, f'Order #{order.transaction_uuid} placed.')
        return redirect('order_detail', pk=order.id)

    return redirect('view_cart')


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    return render(request, 'order/order_detail.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user, status='confirmed')
    return render(request, 'order/my_orders.html', {'orders': orders})