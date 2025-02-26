import pytest

from api.v1.sync.services.handle_terminal_session.add_scanned_products import AddScanProdsToTaskService
from apps.product.models import ScannedProduct


pytestmark = [pytest.mark.django_db]


def test_add_scanned_products(task_for_test_add_scanned_products):
    """Тест для проверки сервиса добавления отсканированных товаров в таску."""
    scanned_products = [
        {
            'product': '222',
            'amount': 2,
            'scanned_time': '2024-05-06T08:56:03.448Z',
            'is_weight_product': False,
            'added_by_product_code': True,
            'added_by_qr_code': False,
            'dm': '123',
            'title': 'Продукт',
            'vendor_code': '333',
            'qr_code': 'http://qr_code_1',
        },
        {
            'product': '567',
            'amount': 7,
            'scanned_time': '2024-05-06T08:57:03.448Z',
            'is_weight_product': False,
            'added_by_product_code': True,
            'added_by_qr_code': False,
            'title': 'Товар',
            'vendor_code': '321',
            'qr_code': 'http://qr_code_2',
        },
        {
            'product': '000',
            'amount': 1000,
            'scanned_time': '2024-05-06T08:58:03.448Z',
            'is_weight_product': True,
            'added_by_product_code': True,
            'added_by_qr_code': False,
            'title': 'Весовой',
            'vendor_code': '999',
            'qr_code': 'http://qr_code_3',
        },
        {
            'product': '567',
            'amount': 2,
            'scanned_time': '2024-05-06T08:59:03.448Z',
            'is_weight_product': False,
            'added_by_product_code': True,
            'added_by_qr_code': False,
            'title': 'Товар',
            'vendor_code': '321',
            'qr_code': 'http://qr_code_4',
        },
    ]
    AddScanProdsToTaskService(task_for_test_add_scanned_products, scanned_products).process()

    # scanned_unknown_product = ScannedProduct.objects.get(product__title='Неизвестный товар')
    # count_scanned_products = ScannedProduct.objects.count()
    # scanned_product_existing = ScannedProduct.objects.get(product__title='Товар')
    #
    # assert task_for_test_add_scanned_products.result == 17
    # assert scanned_unknown_product.product.vendor_code.startswith('art_')
    # assert count_scanned_products == 3
    # assert scanned_product_existing.amount == 14
