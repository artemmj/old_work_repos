import pytest

from api.v1.reports.services import AuditorReportService
from apps.document.models import DocumentStatusChoices

pytestmark = [pytest.mark.django_db]


def test_content_for_auditor_controller(employee_for_auditor_report):
    """Тест для проверки данных в отчете Аудитора с ролью аудитор УК."""
    payload = {
        'excel': False,
        'auditor': employee_for_auditor_report.id,
        'task_type': 'auditor_controller'

    }
    content_for_report = AuditorReportService(
        payload,
        'http://localhost',
    )._prepare_content_for_auditor_controller_report()

    assert content_for_report['statistic']['verified_zones_count'] == 2
    assert content_for_report['zones'][0]['is_result_discrepancy'] == 'Да'


def test_content_for_auditor(employee_for_auditor_report):
    """Тест для проверки данных в отчете Аудитора с ролью аудитор."""
    payload = {
        'excel': False,
        'auditor': employee_for_auditor_report.id,
        'task_type': 'auditor'
    }
    content_for_report = AuditorReportService(
        payload,
        'http://localhost',
    )._prepare_content_for_auditor_report()

    assert content_for_report['statistic']['verified_zones_count'] == 2
    assert content_for_report['zones'][0]['quantity_discrepancy'] == 10
    assert content_for_report['statistic']['scanned_products_count'] == 12


def test_total_scanned_products_by_auditor(employee_for_auditor_report):
    """Тест для проверки общей суммы отсканированных товаров аудитором"""
    documents = employee_for_auditor_report.documents
    payload = {
        'excel': False,
        'auditor': employee_for_auditor_report.id,
        'task_type': 'auditor'
    }
    total_scanned_products_by_auditor = AuditorReportService(
        payload,
        'http://localhost',
    )._scanned_products_count_for(documents)

    assert total_scanned_products_by_auditor == 18


def test_percent_of_scanned_areas(employee_for_auditor_report):
    """Тест для проверки процента отсканированных зон аудитором"""
    documents = employee_for_auditor_report.documents.filter(
        auditor_task__employee=employee_for_auditor_report,
        zone__project=employee_for_auditor_report.project,
        status=DocumentStatusChoices.READY,
    )
    payload = {
        'excel': False,
        'auditor': employee_for_auditor_report.id,
        'task_type': 'auditor'
    }
    percent_of_scanned_areas = AuditorReportService(
        payload,
        'http://localhost',
    )._calculate_percentage_of_scanned_areas(documents)

    assert percent_of_scanned_areas == float(100)
