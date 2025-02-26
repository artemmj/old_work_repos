import shutil

import pytest
from django.test import override_settings
from rest_framework.exceptions import ValidationError

from apps.file.models import File
from apps.file.services import UnzipService

pytestmark = [pytest.mark.django_db]


@override_settings(MEDIA_ROOT='')
def test_unzip(files_factory):
    """Тест для проверки открытия zip файла."""
    filepath = 'apps/file/tests/tests_services/backup_тест.zip'
    files_factory(
        count=1,
        file=filepath,
    )
    file_id = File.objects.first().id

    backup_content = UnzipService(file_id).process()

    assert backup_content == {
        'project': {
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
        'terminal_settigns': {
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
                'is_auto_assignment': True,
                'tasks': [
                    {
                        'id': '8edf832e-de5c-4a76-9da5-d9ef25053081',
                        'terminal': None,
                        'zone': '32566566-2add-478f-b4fd-fbc82aa4251c',
                        'type': 'counter_scan',
                        'status': 'initialized',
                        'result': '12.000',
                        'employee': '2ef7b9e4-6b76-4232-a846-ea667bd03b39',
                        'scanned_products': [
                            {
                                'created_at': '2024-06-25T14:20:19.551376+03:00',
                                'scanned_time': None,
                                'product': '64e1c858-64f1-4e38-ae50-a22150947db7',
                                'amount': '12.000',
                                'added_by_product_code': False
                            }
                        ]
                    },
                    {
                        'id': 'c6d004c5-491a-4205-a44b-7c56989681af',
                        'terminal': None,
                        'zone': '32566566-2add-478f-b4fd-fbc82aa4251c',
                        'type': 'auditor',
                        'status': 'worked',
                        'result': '23.000',
                        'employee': '2ef7b9e4-6b76-4232-a846-ea667bd03b39',
                        'scanned_products': []
                    }
                ]
            }
        ],
        'documents': [
            {
                'fake_id': 1,
                'created_at': '2024-06-25T14:20:19.552944+03:00',
                'employee': None,
                'status': 'ready',
                'zone': '32566566-2add-478f-b4fd-fbc82aa4251c',
                'terminal': None,
                'counter_scan_task': None,
                'controller_task': None,
                'auditor_task': None,
                'auditor_controller_task': None,
                'storage_task': None,
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

    path_folder = 'apps/file/tests/tests_services/backup_тест'
    shutil.rmtree(path_folder)


@override_settings(MEDIA_ROOT='')
def test_unzip_invalid_format_file(files_factory):
    """Тест для проверки неверного формата файла."""
    filepath = 'apps/file/tests/tests_services/invalid_format.txt'
    files_factory(
        count=1,
        file=filepath,
    )
    file_id = File.objects.first().id

    with pytest.raises(ValidationError):
        UnzipService(file_id).process()
