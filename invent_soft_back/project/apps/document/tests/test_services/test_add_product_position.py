from decimal import Decimal

import pytest

from api.v1.document.services import AddProductPositionService
from apps.document.asserts import assert_change_statuses

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'barcode, amount, total_amount, count',
    [
        ('2222', 3, Decimal(3), 2),
        ('3333', 3, Decimal(4), 1),
    ]
)
def test_add_product_position_in_document_and_change_statuses(
    document_for_add_product_position,
    barcode: str,
    amount: int,
    total_amount: Decimal,
    count: int,
):
    """
    Тест для проверки добавления позиции отсканированного товара в документ и смену статусов.

    barcode - штрих-код товара
    amount - кол-во добавляемого отсканированного товара в документ
    total_amount - общее кол-во отсканированного товара в документе
    count - кол-во отсканированных товаров в документе
    """
    serializer_data = {
        'barcode': barcode,
        'amount': amount,
    }
    document = AddProductPositionService(document_for_add_product_position, serializer_data).process()

    assert_change_statuses(document)
    assert document.counter_scan_task.scanned_products.count() == count
    assert document.counter_scan_task.scanned_products.get(product__barcode=barcode).amount == total_amount
