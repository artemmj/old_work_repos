import pytest

from api.v1.reports.services import DiscAccountingQuantityReportService

pytestmark = [pytest.mark.django_db]


def test_disc_accounting_quantity_report(project_for_disc_accounting_quantity_report):
    """Тест для проверки расхождения товаров и разницы в цене в отчете Расхождение с учетным количеством."""
    payload = {
        'project': project_for_disc_accounting_quantity_report.id,
        'excel': False,
        'group_by': 'by_barcode',
    }
    context = DiscAccountingQuantityReportService(payload, 'http://localhost')._create_context()

    assert context['alls_fact'] == float(11)
    assert context['alls_uchet'] == float(9)
    assert context['alls_price_amount'] == float(1000)
