import pytest

from api.v1.reports.services import SuspiciousBarcodesReportService


pytestmark = [pytest.mark.django_db]


def test_suspicious_barcodes_report(project_suspicious_barcodes_report):
    """Тест для проверки кол-во товаров с подозрительным ШК в Отчете по подозрительным ШК."""
    payload = {
        'project': project_suspicious_barcodes_report.id,
        'excel': False,
    }
    context = SuspiciousBarcodesReportService(payload, 'http://localhost')._create_context()

    assert len(context['products']) == 2
