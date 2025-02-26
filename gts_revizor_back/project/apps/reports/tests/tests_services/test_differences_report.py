import pytest

from api.v1.reports.services import DifferencesReportService


pytestmark = [pytest.mark.django_db]


def test_differences_report_surplus_sum_and_shortage_sum(project_for_differences_report):
    """Тест проверки суммы излишек и недостачи отчета Ре Трейдинг счислительная (Отчет по расхождениям). """
    payload = {
        'excel': False,
        'project': project_for_differences_report.id
    }
    context = DifferencesReportService(payload, 'http://localhost')._create_context()

    assert context['alls_surplus_sum'] == float(3000)
    assert context['alls_shortage_sum'] == float(2000)
