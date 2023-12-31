from cart.views import cart_add, cart_remove, cart_detail
from my_shop.models import Category, Product
from django.test import TestCase, RequestFactory
from cart.cart import Cart



class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category', slug='test-category')

    def test_name_label(self):
        category = Category.objects.first()
        category.name = category._meta.get_field('name').verbose_name
        category.slug = category._meta.get_field('slug').verbose_name
        self.assertEquals(category.name, 'Название')
        self.assertEquals(category.slug, 'Сокращ_урл')

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category', slug='test-category')
        category = Category.objects.first()
        Product.objects.create(category=category, name='Test Product', slug='test-product', price=1, stock=1)

    def test_name_label(self):
        product = Product.objects.first()
        product.name = product._meta.get_field('name').verbose_name
        product.price = product._meta.get_field('price').verbose_name
        self.assertEquals(product.name, 'Название')
        self.assertEquals(product.price, 'Цена')

class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        response = self.client.get('http://127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)

class CartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Category.objects.create(name='Test Category', slug='test-category')
        cat = Category.objects.first()
        self.product = Product.objects.create(
            name='Test Product',
            price=10,
            stock=1,
            category=cat)

    def test_cart_add(self):
        request = self.factory.post('/cart/add/', {'quantity': 1, 'update': False})
        self.session = request.session
        response = cart_add(request, product_id=self.product.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/cart_detail/')

    def test_cart_remove(self):
        request = self.factory.post('/cart/remove/', {})
        self.session = request.session
        Cart(request).add(product=self.product, quantity=1)
        response = cart_remove(request, product_id=self.product.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/cart_detail/')

    def test_cart_detail(self):
        request = self.factory.get('/cart/detail/')
        self.session = request.session
        Cart(request).add(product=self.product, quantity=1)
        response = cart_detail(request)
        self.assertEqual(response.status_code, 200)




