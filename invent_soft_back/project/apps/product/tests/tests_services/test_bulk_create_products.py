import pytest

from apps.product.models import Product
from apps.product.services import BulkCreateProductsService

pytestmark = [pytest.mark.django_db]


def test_bulk_create_products(project):
    """Тест для проверки массового создания продуктов."""
    products_content = [
        {
            'id': '54383f51-6ad8-53d4-ae1d-579c1ac3f9d3',
            'vendor_code': '711291001',
            'barcode': '2100000524792',
            'title': 'Продукт 1',
            'remainder': '0.000',
            'price': '0.00',
            'am': None,
            'dm': None,
        },
        {
            'id': 'fd211a94-15eb-5a94-b82d-b5bee412136c',
            'vendor_code': '711291012',
            'barcode': '2100000524969',
            'title': 'Продукт 2',
            'remainder': '0.000',
            'price': '0.00',
            'am': None,
            'dm': None,
        },
    ]

    BulkCreateProductsService(project, products_content).process()

    assert Product.objects.filter(project=project).count() == 2
