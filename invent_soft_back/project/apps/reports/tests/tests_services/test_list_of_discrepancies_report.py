from decimal import Decimal

import pytest

from api.v1.reports.services import ListOfDiscrepanciesReportService


pytestmark = [pytest.mark.django_db]


def test_list_of_discrepancies_report_all_fact_diff_count_and_diff_price(project_list_of_discrepancies_report):
    """
    Тест для проверки фактического наличия, расхождения и суммы товаров в отчете Ведомость расхождения Концепт Груп
    """
    payload = {
        'project': project_list_of_discrepancies_report.id,
        'excel': False,
        'only_discrepancies': False,
    }

    context = ListOfDiscrepanciesReportService(payload, 'http://localhost')._create_context()

    assert context['alls_fact_count'] == Decimal(13)
    assert context['alls_diff_count'] == Decimal(4)
    assert context['alls_diff_price'] == Decimal(2000)
