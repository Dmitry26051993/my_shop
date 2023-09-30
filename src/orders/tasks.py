import email
from io import BytesIO
import weasyprint
from celery import shared_task
from django.core.mail import send_mail
from orders.models import Order
from django.template.loader import render_to_string


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Номер заказа {order.id}'
    message = f'Уважаемый {order.first_name},\n\n' \
              f'Вы успешно разместили заказ' \
              f'Ваш идентификатор заказа - это {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'dmartynovic2@gmail.com',
                          [order.email])
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    from django.conf import settings
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # send e-mail
    email.send()
    return mail_sent