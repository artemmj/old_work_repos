import pytest

from apps.product.models import Product, ScannedProduct
from apps.product.services import BulkCreateScannedProductsService
from apps.task.models import Task

pytestmark = [pytest.mark.django_db]


def test_bulk_create_scanned_products(project_for_bulk_create_scanned_products):
    """Тест для проверки массового создания отсканированных продуктов."""
    product_1_id = Product.objects.filter(project=project_for_bulk_create_scanned_products, barcode='111').first().id
    product_2_id = Product.objects.filter(project=project_for_bulk_create_scanned_products, barcode='222').first().id
    task_id = Task.objects.filter(zone__project=project_for_bulk_create_scanned_products).first().id
    scanned_products = [
        {
            'id': '1affc1bb-a7e6-4f78-87dc-01eae952988e',
            'created_at': '2024-05-27T12:35:20.178724+03:00',
            'scanned_time': '2024-05-27T20:30:12+03:00',
            'product_id': product_1_id,
            'amount': '1.000',
            'added_by_product_code': False,
            'task_id': task_id,
        },
        {
            'id': '054aa623-312a-47d5-bff4-584c82453a2a',
            'created_at': '2024-05-27T12:35:20.159548+03:00',
            'scanned_time': '2024-05-27T20:30:09+03:00',
            'product_id': product_2_id,
            'amount': '2.000',
            'added_by_product_code': False,
            'task_id': task_id,
        },
    ]

    BulkCreateScannedProductsService(scanned_products).process()

    assert ScannedProduct.objects.filter(product__project=project_for_bulk_create_scanned_products).count() == 2
