from django.contrib import admin
from .models import Item, Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
