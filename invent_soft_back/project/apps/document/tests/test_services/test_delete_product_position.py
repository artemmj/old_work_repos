import pytest

from api.v1.document.services import DeleteProductPositionService
from apps.document.asserts import assert_change_statuses
from apps.product.models import ScannedProduct


pytestmark = [pytest.mark.django_db]


def test_delete_product_position_and_change_statuses(document_for_delete_product_position):
    """Тест для проверки сервиса удаления позиции отсканированного товара в документе и смену статусов."""
    scanned_product = ScannedProduct.objects.get(product__title='Test')
    serializer_data = {
        'product': scanned_product.id,
    }
    document = DeleteProductPositionService(document_for_delete_product_position, serializer_data).process()

    assert_change_statuses(document)
    assert document.counter_scan_task.scanned_products.count() == 2
    assert document.counter_scan_task.result == 2
