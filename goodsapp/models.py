from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Item(models.Model):
    """Модель товаров"""
    name = models.CharField(max_length=128, verbose_name='Название')
    description = models.CharField(max_length=255, verbose_name='Описание', **NULLABLE)
    price = models.IntegerField(default=0, verbose_name='Стоимость')

    def __str__(self):
        return f'{self.name}({self.price / 100})'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']

    def get_display_price(self):
        return '{0:.2f}'.format(self.price / 100)


class Order(models.Model):
    """Модель заказа"""
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-id']


class OrderItem(models.Model):
    """Модель сущностей заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    @property
    def product_cost(self):
        return self.product.price * self.quantity
