from django.db import models
from my_shop.models import Product
from django.core.validators import RegexValidator

class Order(models.Model):
    first_name = models.CharField(max_length=15, verbose_name='Имя')
    last_name = models.CharField(max_length=25, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Электронная почта')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message='Номер телефона должен быть введен в формате: "+999999999". Допускается до 15 цифр.')
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='Номер телефона')
    address = models.CharField(max_length=75, verbose_name='Адрес')
    city = models.CharField(max_length=30, verbose_name='Город')
    comment = models.TextField(verbose_name='Комментарий к заказу')
    paid = models.BooleanField(default=False, verbose_name='Создано')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity