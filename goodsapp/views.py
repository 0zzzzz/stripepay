import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionAPIView(APIView):
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
                }
            ],
            mode='payment',
            success_url=f'http://{request.build_absolute_uri().split("/")[2]}/success/',
            cancel_url=f'http://{request.build_absolute_uri().split("/")[2]}/cancel/',
        )

        return redirect(checkout_session.url)


class ItemBuyAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'item_buy.html'

    def get(self, request, pk):
        item = Item.objects.get(id=pk)
        return Response(
            {'item': item, 'title': item.name},
            content_type='text/html',
        )


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'
