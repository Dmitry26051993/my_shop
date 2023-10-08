from django.shortcuts import render, get_object_or_404
from orders.models import OrderItem, Order
from orders.forms import OrderCreateForm
from cart.cart import Cart
from django.http import HttpResponse
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from orders.tasks import order_created

def order_create(request):
    current_time = datetime.now().time()
    if current_time.hour < 8 or current_time.hour > 22:
        return HttpResponse('Сервис не доступен для заказов. Пожалуйста, вернитесь с 8 утра до 22 вечера.')
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

