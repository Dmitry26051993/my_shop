from celery import shared_task
from django.core.mail import send_mail
from orders.models import Order


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Номер заказа {order.id}'
    message = f'Уважаемый  клиент{order.first_name},\n\n' \
              f'Вы успешно разместили заказ'  \
              f'Ваш идентификатор заказа - это {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'dmartynovic2@gmail.com',
                          [order.email])

    return mail_sent