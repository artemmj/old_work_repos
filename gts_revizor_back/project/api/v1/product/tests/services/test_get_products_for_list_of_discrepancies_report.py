import pytest

from api.v1.product.services import GetProductsForListOfDiscrepanciesReportsService

pytestmark = [pytest.mark.django_db]



def test_get_products_for_list_discrepancies_reports_successful(project, products_factory):
    """Тест для проверки  получения кол-ва продуктов для отчета "Концепт групп"."""
    products_factory(
        count=3,
        project=project,
        title=(title for title in ['Test', 'Test_2', 'Неизвестный товар']),
        remainder=(remainder for remainder in [5, None, 6]),
        remainder_2=(remainder_2 for remainder_2 in [1, 5, None]),
        barcode=(barcode for barcode in ['3333', '2222', '1111']),
        vendor_code=(vendor_code for vendor_code in ['9999', '8888', '7777'])
    )
    products_count = GetProductsForListOfDiscrepanciesReportsService(project).process()

    assert products_count.count() == 1
