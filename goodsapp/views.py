import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionAPIView(APIView):
    """Создает сеанс оформления заказа на сервисе stripe"""
    def get(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs["pk"])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name
                        },
                    },
                    'quantity': 1
                },
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name
                        },
                    },
                    'quantity': 1
                }
            ],
            mode='payment',
            success_url=f'http://{request.build_absolute_uri().split("/")[2]}/success/',
            cancel_url=f'http://{request.build_absolute_uri().split("/")[2]}/cancel/',
        )

        return redirect(checkout_session.url)


class CreateCheckoutSessionFromOrderAPIView(APIView):
    """Создает сеанс оформления заказа на сервисе stripe из модели заказа"""
    def get(self, request, *args, **kwargs):
        order = OrderItem.objects.filter(order=self.kwargs["pk"])
        order_list = []
        for order_item in order:
            order_list.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': order_item.product.price,
                        'product_data': {
                            'name': order_item.product.name
                        },
                    },
                    'quantity': order_item.quantity
                })
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=order_list,
            mode='payment',
            success_url=f'http://{request.build_absolute_uri().split("/")[2]}/success/',
            cancel_url=f'http://{request.build_absolute_uri().split("/")[2]}/cancel/',
        )

        return redirect(checkout_session.url)

class ItemBuyAPIView(APIView):
    """Простая страница заказа, позволяет купить продукт"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'item_buy.html'

    def get(self, request, pk):
        item = Item.objects.get(id=pk)
        return Response(
            {'item': item, 'title': item.name},
            content_type='text/html',
        )

class OrderBuyAPIView(APIView):
    """Простая страница заказа, позволяет купить один продукт"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order_buy.html'
    def get(self, request, pk):
        order = OrderItem.objects.filter(order=pk)
        return Response(
            {'order': order, 'title': 'заказ', 'order_pk': pk},
            content_type='text/html',
        )


class SuccessView(TemplateView):
    """Страница сигнализирующая об отмене сеанса оформления заказа"""
    template_name = 'success.html'


class CancelView(TemplateView):
    """Страница сигнализирующая об успешном оформлении заказа"""
    template_name = 'cancel.html'
