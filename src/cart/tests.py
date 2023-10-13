from cart.views import cart_add, cart_remove, cart_detail
from my_shop.models import Category, Product
from my_shop.views import product_list, product_detail
from django.test import TestCase, RequestFactory
from orders.models import OrderItem, Order
from cart.cart import Cart
from orders.views import order_create, admin_order_detail


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category', slug='test-category')

    def test_name_label(self):
        category = Category.objects.get()
        category.name = category._meta.get_field('name').verbose_name
        category.slug = category._meta.get_field('slug').verbose_name
        self.assertEquals(category.name, 'Название'), (category.slug, 'Сокращ_урл')

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category', slug='test-category')
        category = Category.objects.get(id=1)
        Product.objects.create(category=category, name='Test Product', slug='test-product', price=1, stock=1)

    def test_name_label(self):
        product = Product.objects.get(id=1)
        product.name = product._meta.get_field('name').verbose_name
        product.price = product._meta.get_field('price').verbose_name
        self.assertEquals(product.name, 'Название'), (product.price, 'Цена')

class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        response = self.client.get('http://127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)

class CartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        Category.objects.create(name='Test Category', slug='test-category')
        cat = Category.objects.get(id=1)
        self.product = Product.objects.create(
            name='Test Product',
            price=10,
            stock=1,
            category=cat)

    def test_cart_add(self):
        request = self.factory.post('/cart/add/', {'quantity': 1, 'update': False})
        request.session = {}
        response = cart_add(request, product_id=self.product.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/cart_detail/')

    def test_cart_remove(self):
        request = self.factory.post('/cart/remove/', {})
        request.session = {}
        Cart(request).add(product=self.product, quantity=1)
        response = cart_remove(request, product_id=self.product.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/cart_detail/')

    def test_cart_detail(self):
        request = self.factory.get('/cart/detail/')
        request.session = {}
        Cart(request).add(product=self.product, quantity=1)
        response = cart_detail(request)
        self.assertEqual(response.status_code, 200)

class ProductTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        Category.objects.create(name='Test Category', slug='test-category')
        cat = Category.objects.get(id=1)

        self.product = Product.objects.create(
            name='Test Product',
            price=10,
            stock=1,
            category=cat)

    def test_product_list(self):
        request = self.factory.get('/product/list/')
        response = product_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
        self.assertContains(response, 'Test Product')

    def test_product_detail(self):
        request = self.factory.get('/product/detail/')
        response = product_detail(request, id=self.product.id, slug=self.product.slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

class OrderTestCase(TestCase):

    def test_order_create(self):
        request = self.factory.post('/order/create/', {'first_name': 'Test', 'last_name': 'Test', 'email': 'test@example.com', 'phone': '+3752222653', 'address': 'Test address',  'city': 'Test city', 'comment': 'test'})
        request.session = {}
        Cart(request).add(product=self.product, quantity=1)
        response = order_create(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_admin_order_detail(self):
        request = self.factory.get('/admin/order/detail/')
        request.user = self.user
        order = Order.objects.create(first_name='Test', last_name='Test', email='test@example.com', phone='+3752222653', address='Test address',  city='Test city', comment='test')
        OrderItem.objects.create(order=order, product=self.product, price=10, quantity=1)
        response = admin_order_detail(request, order_id=order.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
