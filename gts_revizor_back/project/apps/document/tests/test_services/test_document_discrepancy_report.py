import pytest

from api.v1.document.services import DocumentDiscrepancyReportService

pytestmark = [pytest.mark.django_db]


def test_discrepancy_report(document_discrepancy_report):
    """Тест для проверки отчета по расхождениям в ходе фискальной инвентаризации"""
    context = DocumentDiscrepancyReportService(
        document_discrepancy_report.id,
        'http://localhost',
    )._create_context_for_report()

    assert len(context['scanned_products']) == 3
    assert context['scanned_products'][1]['discrepancy'] == '*'
