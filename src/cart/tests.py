from http import HTTPStatus
from django.test import Client, TestCase

from my_shop.models import Product


class StaticURLTests(TestCase):
    def setUp(self) -> None:
        self.guest_client = Client()

    def test_static_page(self) -> None:
        pages: tuple = ('/about/author/', '/about/tech/')
        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_uses_correct_template(self) -> None:
        templates_url_names: dict = {
            'product_id': 'my_shop/product/list.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                error_name: str = f'Ошибка: {adress} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)

class ProductTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.actor = Product.objects.create(
            name="John",
            price="10.5")





