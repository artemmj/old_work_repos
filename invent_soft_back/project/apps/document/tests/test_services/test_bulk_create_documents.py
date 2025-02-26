import pytest

from apps.document.models import Document
from apps.document.services import BulkCreateDocumentsService
from apps.employee.models import Employee
from apps.terminal.models import Terminal
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_bulk_create_documents(project_for_bulk_create_documents):
    """Тест для проверки массового создания документов."""
    terminal_id = Terminal.objects.filter(
        project=project_for_bulk_create_documents,
    ).first().id
    zone_id = Zone.objects.filter(
        project=project_for_bulk_create_documents,
    ).first().id
    employee_id = Employee.objects.filter(
        project=project_for_bulk_create_documents,
    ).first().id
    documents_content = [
        {
            'fake_id': 1,
            'created_at': '2024-06-25T14:00:20.250612+03:00',
            'employee_id': employee_id,
            'status': 'ready',
            'zone_id': zone_id,
            'terminal_id': terminal_id,
            'counter_scan_task_id': None,
            'controller_task_id': None,
            'auditor_task_id': None,
            'auditor_controller_task_id': None,
            'storage_task': None,
            'start_audit_date': None,
            'end_audit_date': None,
            'tsd_number': None,
            'suspicious': False,
            'color': 'red',
            'color_changed': False,
        },
        {
            'fake_id': 2,
            'created_at': '2024-06-25T14:20:20.250612+03:00',
            'employee_id': employee_id,
            'status': 'ready',
            'zone_id': zone_id,
            'terminal_id': terminal_id,
            'counter_scan_task_id': None,
            'controller_task_id': None,
            'auditor_task_id': None,
            'auditor_controller_task_id': None,
            'storage_task_id': None,
            'start_audit_date': None,
            'end_audit_date': None,
            'tsd_number': None,
            'suspicious': False,
            'color': 'red',
            'color_changed': False,
        },
    ]

    BulkCreateDocumentsService(documents_content).process()

    assert Document.objects.filter(zone__project=project_for_bulk_create_documents).count() == 2
