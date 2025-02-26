import pytest
from django.test import override_settings

from apps.file.models import File
from apps.project.tasks.import_project_service_new import ImportProjectNewService

pytestmark = [pytest.mark.django_db]


@override_settings(MEDIA_ROOT='')
def test_import_project_new(files_factory):
    """Тест для проверки импорта проекта."""
    filepath = 'apps/project/tests/test_services/test_import_project_new/backup_тест.zip'
    files_factory(
        count=1,
        file=filepath,
    )
    file_id = File.objects.first().id
    backup_content = {
        'project': {
            'id': '86a45ed6-92ea-413c-8b13-c30294be171b',
            'title': 'тест',
            'created_at': '2024-06-25T14:20:19.534384+03:00',
            'address': '123'
        },
        'manager': {
            'id': '6f47ac5c-9ab0-4717-9b37-08170023a729',
            'phone': '+79270000001',
            'username': '',
            'first_name': 'admin,',
            'middle_name': 'admin,',
            'last_name': 'admin,'
        },
        'terminal_settings': {
            'issuing_task': 'least_loaded_user',
            'length_barcode_pallets': 0,
            'error_correction': False,
            'compliance_codes': '0-000;1-770;2-780,3-020;4-021;5-022;6-023;7-024;8-025;9-026',
            'product_name': 'by_product_code',
            'unknown_barcode': 'disallow',
            'trimming_barcode': 0,
            'recalculation_discrepancy': 'scan',
            'suspicious_barcodes_amount': 15,
            'check_dm': 'without_dm_check',
            'check_am': 'without_am_check',
            'search_by_product_code': False,
            'manual_input_quantity': False
        },
        'rmm_settings': {
            'auto_zones_amount': 0,
            'password': '555',
            'norm': None,
            'extended_tasks': False
        },
        'employees': [
            {
                'id': '2ef7b9e4-6b76-4232-a846-ea667bd03b39',
                'serial_number': 1,
                'username': 'Сотрудник1',
                'roles': [
                    'counter'
                ],
                'is_deleted': False
            }
        ],
        'terminals': [],
        'products': [
            {
                'id': '64e1c858-64f1-4e38-ae50-a22150947db7',
                'vendor_code': '123',
                'barcode': '123',
                'title': '123',
                'remainder': '0.000',
                'price': '23.00',
                'am': None,
                'dm': None
            }
        ],
        'zones': [
            {
                'id': '32566566-2add-478f-b4fd-fbc82aa4251c',
                'serial_number': 1,
                'title': '123',
                'storage_name': '123',
                'code': '123',
                'status': 'ready',
                'is_auto_assignment': True
            }
        ],
        'tasks': [
            {
                'id': '8edf832e-de5c-4a76-9da5-d9ef25053081',
                'terminal_id': None,
                'zone_id': '32566566-2add-478f-b4fd-fbc82aa4251c',
                'type': 'counter_scan',
                'status': 'initialized',
                'result': '12.000',
                'employee_id': '2ef7b9e4-6b76-4232-a846-ea667bd03b39'
            },
            {
                'id': 'c6d004c5-491a-4205-a44b-7c56989681af',
                'terminal_id': None,
                'zone_id': '32566566-2add-478f-b4fd-fbc82aa4251c',
                'type': 'auditor',
                'status': 'worked',
                'result': '23.000',
                'employee_id': '2ef7b9e4-6b76-4232-a846-ea667bd03b39'
            }
        ],
        'scanned_products': [
            {
                'id': '18dfbd47-c24b-4137-abec-1ade0536aa07',
                'created_at': '2024-06-25T14:20:19.551376+03:00',
                'scanned_time': None,
                'product_id': '64e1c858-64f1-4e38-ae50-a22150947db7',
                'amount': '12.000',
                'added_by_product_code': False,
                'task_id': '8edf832e-de5c-4a76-9da5-d9ef25053081'
            }
        ],
        'documents': [
            {
                'fake_id': 1,
                'created_at': '2024-06-25T14:20:19.552944+03:00',
                'employee_id': None,
                'status': 'ready',
                'zone_id': '32566566-2add-478f-b4fd-fbc82aa4251c',
                'terminal_id': None,
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
                'color_changed': False
            }
        ],
        'events': [
            {
                'fake_id': 1,
                'created_at': '2024-06-25T14:20:19.555681+03:00',
                'title': 'import_project',
                'comment': 'Импортирован проект из файла DyD7NWL96StDEg.zip'
            }
        ],
        'product_title_attrs': []
    }

    new_project_title = ImportProjectNewService(backup_content, file_id).process()

    assert new_project_title == 'тест'
