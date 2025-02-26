from decimal import Decimal

import pytest

from api.v1.reports.services import DiscrepanciesReportService

pytestmark = [pytest.mark.django_db]


def test_discrepancies_report_all_diff_amount_and_price(project_for_discrepancies_report):
    """Тест для проверки расхождения кол-во и суммы товаров в отчете L&G сличительная (Ведомость расхождений)."""
    payload = {
        'project': project_for_discrepancies_report.id,
        'excel': False,
    }
    context = DiscrepanciesReportService(payload, 'http://localhost')._create_context_for_report()

    assert context['alls_diff_amount'] == Decimal(10)
    assert context['alls_diff_price'] == Decimal(1000)


def test_discrepancies_report_add_art_in_vendor_code(project_for_discrepancies_report):
    """
    Тест для проверки прибавления префикса art_ в vendor_code при его отсуствии
    в отчете L&G сличительная (Ведомость расхождений).
    """
    payload = {
        'project': project_for_discrepancies_report.id,
        'excel': False,
    }
    context = DiscrepanciesReportService(payload, 'http://localhost')._create_context_for_report()

    assert context['products'][0]['vendor_code'].startswith('art_')
    assert context['products'][1]['vendor_code'].startswith('art_') is False
