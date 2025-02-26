import pytest

from apps.file.models import File
from apps.project.tasks.import_zones import ImportZonesService
from apps.template.models import Template
from django.test import override_settings

pytestmark = [pytest.mark.django_db]


@override_settings(MEDIA_ROOT='')
def test_prepare_create_zones(project_for_import_zones_service):
    """Тест для проверки функции _prepare_create_zones сервиса ImportZonesService"""
    template = Template.objects.first()
    file = File.objects.first()

    serializer_data = {
        'project': project_for_import_zones_service.id,
        'template': template.id,
        'file': file.id
    }

    create_zones, reader = ImportZonesService(serializer_data)._prepare_create_zones(5, template)

    assert create_zones[-1]['serial_number'] == 10
    assert len(create_zones) == 5
    assert reader.line_num == 5
