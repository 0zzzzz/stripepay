from django.contrib import admin
from django.urls import path
from goodsapp.views import (
    CancelView,
    SuccessView,
    CreateCheckoutSessionAPIView,
    ItemBuyAPIView,
    CreateCheckoutSessionFromOrderAPIView,
    OrderBuyAPIView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('item/<int:pk>/', ItemBuyAPIView.as_view(), name='item_by'),
    path('order/<int:pk>/', OrderBuyAPIView.as_view(), name='item_by'),
    path('buy/<int:pk>/', CreateCheckoutSessionAPIView.as_view(), name='create-checkout-session'),
    path('buy_order/<int:pk>/', CreateCheckoutSessionFromOrderAPIView.as_view(), name='create-checkout-session-order'),
]
