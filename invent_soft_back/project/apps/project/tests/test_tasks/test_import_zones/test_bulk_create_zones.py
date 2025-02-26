import pytest

from apps.file.models import File
from apps.project.tasks.import_zones import ImportZonesService
from apps.template.models import Template
from django.test import override_settings

from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


@override_settings(MEDIA_ROOT='')
def test_bulk_create_zones(project_for_import_zones_service):
    """Тест для проверки функции _bulk_create_zone сервиса ImportZonesService"""
    create_zones = [
        {'code': '1', 'serial_number': 6, 'title': ' zone 1'},
        {'code': '2', 'serial_number': 7, 'title': ' zone 2'},
        {'code': '3', 'serial_number': 8, 'title': ' zone 3'},
        {'code': '4', 'serial_number': 9, 'title': ' zone 4'},
        {'code': '5', 'serial_number': 10, 'title': ' zone 5'},
    ]
    template = Template.objects.first()
    file = File.objects.first()

    serializer_data = {
        'project': project_for_import_zones_service.id,
        'template': template.id,
        'file': file.id
    }

    ImportZonesService(serializer_data)._bulk_create_zones(create_zones)

    assert Zone.objects.count() == 10
