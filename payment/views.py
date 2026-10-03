from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
import stripe

from cart.models import Order  # Використовуємо лише актуальні моделі

# Налаштування Stripe API
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = getattr(settings, 'STRIPE_API_VERSION', '2023-10-16')  # Виправлено: STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)  # Виправлено: правильне отримання замовлення

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:success'))  # Виправлено name
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))  # Виправлено name

        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []  # Виправлено: line_items замість line_item
        }

        # Отримуємо товари із замовлення
        for item in order.items.all():  # Виправлено: order.items замість order.item
            session_data['line_items'].append({
                'price_data': {
                    'currency': 'usd',  # Виправлено: currency замість currensy
                    'product_data': {
                        'name': item.product.name,  # Виправлено: item.product.name замість item.post.title
                    },
                    'unit_amount': int(item.price * Decimal('100')),
                },
                'quantity': item.quantity,
            })

        session = stripe.checkout.Session.create(**session_data)  # Виправлено: session_data
        return redirect(session.url, code=303)

    else:
        return render(request, 'payment/process.html', {'order': order})  # Виправлено: order замість oeder


def success(request):
    return render(request, 'payment/success.html')


def canceled(request):
    return render(request, 'payment/canceled.html')


@require_POST
@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('client_reference_id')
        
        try:
            order = Order.objects.get(id=order_id)
            order.payable = True  # або order.paid = 'card' в залежності від ваших полів
            order.save()
        except Order.DoesNotExist:
            return HttpResponse(status=404)

    return HttpResponse(status=200)