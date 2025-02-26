from decimal import Decimal

import pytest

from api.v1.reports.services import ListOfDiscrepanciesReportService

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'only_discrepancies, alls_fact_count, alls_diff_count, alls_diff_price',
    [
        (False, Decimal(14), Decimal(-1), Decimal(-500)),
        (True, Decimal(9), Decimal(-1), Decimal(-500)),

    ]
)
def test_list_of_discrepancies_report_all_fact_diff_count_and_diff_price(
    project_list_of_discrepancies_report,
    only_discrepancies: bool,
    alls_fact_count: Decimal,
    alls_diff_count: Decimal,
    alls_diff_price: Decimal,
):
    """
    Тест для проверки фактического наличия, расхождения и суммы товаров в отчете Ведомость расхождения Концепт Груп

    only_discrepancies - только расхождения
    alls_fact_count - общее фактичкское кол-во
    alls_diff_count - общее кол-во расхождений
    alls_diff_price - общее кол-во суммы
    """
    payload = {
        'project': project_list_of_discrepancies_report.id,
        'excel': False,
        'only_discrepancies': only_discrepancies,
    }

    context = ListOfDiscrepanciesReportService(payload, 'http://localhost')._create_context()

    assert context['alls_fact_count'] == alls_fact_count
    assert context['alls_diff_count'] == alls_diff_count
    assert context['alls_diff_price'] == alls_diff_price
