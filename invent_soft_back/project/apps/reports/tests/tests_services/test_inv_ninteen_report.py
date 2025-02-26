import pytest

from api.v1.reports.services import InvNinteenReportService


pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'include, alls_surplus_sum, alls_shortage_sum',
    [
        ('all', float(3500), float(1500)),
        ('only_identified', float(0), float(3000)),
        ('only_unidentified', float(3000), float(0)),
        ('found_by_product_code', float(500), float(0)),
    ],
)
def test_inv_ninteen_report_all_surplus_sum_and_shortage_sum(
    project_inv_ninteen_report,
    include: str,
    alls_surplus_sum: float,
    alls_shortage_sum: float,
):
    """
    Тест для проверки суммы излишек и недостатков при разных условиях.

    include: all - в отчете все товары
    include: only_identified - в отчете только опознанные товары
    include: only_unidentified - в отчете только неопознанные товары
    include: found_by_product_code - в отчете только товары найденные по коду товара
    alls_surplus_sum - общая сумма излишек
    alls_shortage_sum - общее сумма недостачи
    """
    payload = {
        'project': project_inv_ninteen_report.id,
        'excel': False,
        'include': include,
        'group_by': 'by_barcode',
    }
    context = InvNinteenReportService(payload, 'http://localhost')._create_context()

    assert context['alls_surplus_sum'] == alls_surplus_sum
    assert context['alls_shortage_sum'] == alls_shortage_sum


@pytest.mark.parametrize(
    'group_by, code',
    [
        ('by_barcode', '1111'),
        ('by_product_code', '7777'),
    ],
)
def test_inv_ninteen_report_group_by_barcode_and_vendor_code(project_inv_ninteen_report, group_by: str, code: str):
    """Тест для проверки группировки  по barcode и vendor_code в документе ИНВ-19."""
    payload = {
        'project': project_inv_ninteen_report.id,
        'excel': False,
        'include': 'all',
        'group_by': group_by,
    }

    context = InvNinteenReportService(payload, 'http://localhost')._create_context()

    assert context['products'][0]['code'] == code
