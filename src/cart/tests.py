from django.test import TestCase
from my_shop.models import Category, Product


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category', slug='test-category')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        category.name = category._meta.get_field('name').verbose_name
        category.slug = category._meta.get_field('slug').verbose_name
        self.assertEquals(category.name, 'Название'), (category.slug, 'Сокращ_урл')

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category', slug='test-category')
        category = Category.objects.get(id=1)
        Product.objects.create(category=category, name='Test Product', slug='test-product', price=10.00, stock=100)

    def test_name_label(self):
        product = Product.objects.get(id=1)
        product.name = product._meta.get_field('name').verbose_name
        product.price = product._meta.get_field('price').verbose_name
        self.assertEquals(product.name, 'Название'), (product.price, 'Цена')

class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        response = self.client.get('http://127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)


