import pytest

from apps.file.models import File
from apps.project.tasks.import_zones import ImportZonesService
from apps.template.models import Template
from django.test import override_settings

pytestmark = [pytest.mark.django_db]


@override_settings(MEDIA_ROOT='')
def test_get_last_serial_number(project_for_import_zones_service):
    """Тест для проверки функции _get_last_serial_number сервиса ImportZonesService"""
    template = Template.objects.first()
    file = File.objects.first()

    serializer_data = {
        'project': project_for_import_zones_service.id,
        'template': template.id,
        'file': file.id
    }

    last_serial_number = ImportZonesService(serializer_data)._get_last_serial_number()

    assert last_serial_number == 5
