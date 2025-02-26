import pytest

from api.v1.reports.services import InvThreeReportService

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'include, total_actual_amount, total_number_units',
    [
        ('all', float(4500), float(45)),
        ('only_identified', float(2000), float(20)),
        ('only_unidentified', float(2500), float(25)),
        ('found_by_product_code', float(2000), float(20)),
    ]
)
def test_inv_three_report_total_amount_and_units_successful(
    documents_inv_three_report,
    include: str,
    total_actual_amount: float,
    total_number_units: float,
):
    """
    Тест для проверки кол-ва и общей цены товаров в документе ИНВ-3 при разных условиях.

    include: all - в отчете все товары из готовых документов
    include: only_identified - в отчете только опознанные товары
    include: only_unidentified - в отчете только неопознанные товары
    include: found_by_product_code - в отчете только товары найденные по коду товара
    total_actual_amount - общая цена товаров
    total_number_units - общее кол-во товаров
    """
    payload = {
        'project': documents_inv_three_report[0].zone.project.id,
        'excel': False,
        'include': include,
        'group_by': 'by_barcode',
    }
    source_data = InvThreeReportService(payload, 'http://localhost')._create_context()

    assert source_data['total_actual_amount'] == total_actual_amount
    assert source_data['total_number_units'] == total_number_units


def test_inv_three_report_group_by_barcode(documents_inv_three_report):
    """Тест для проверки группировки  по barcode в документе ИНВ-3."""
    payload = {
        'project': documents_inv_three_report[0].zone.project.id,
        'excel': False,
        'include': 'all',
        'group_by': 'by_barcode',
    }

    source_data = InvThreeReportService(payload, 'http://localhost')._create_context()
    barcode = documents_inv_three_report[0].counter_scan_task.scanned_products.first().product.barcode

    assert source_data['pages'][0]['products'][0]['code'] == barcode


def test_inv_three_report_group_by_vendor_code(documents_inv_three_report):
    """Тест для проверки группировки по vendor_code в документе ИНВ-3."""
    payload = {
        'project': documents_inv_three_report[0].zone.project.id,
        'excel': False,
        'include': 'all',
        'group_by': 'by_product_code',
    }

    source_data = InvThreeReportService(payload, 'http://localhost')._create_context()
    vendor_code = documents_inv_three_report[0].counter_scan_task.scanned_products.first().product.vendor_code

    assert source_data['pages'][0]['products'][0]['code'] == vendor_code
