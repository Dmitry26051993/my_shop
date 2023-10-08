from django.test import TestCase
from my_shop.models import Category, Product

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category', slug='test-category')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_slug_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Сокращ_урл')

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category', slug='test-category')
        category = Category.objects.get(id=1)
        Product.objects.create(category=category, name='Test Product', slug='test-product', price=10.00, stock=100)

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_price_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'Цена')