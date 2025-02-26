import pytest

from apps.file.models import File
from apps.project.tasks.import_zones import ImportZonesService
from apps.template.models import Template
from django.test import override_settings

from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


@override_settings(MEDIA_ROOT='')
def test_import_zones_service(project_for_import_zones_service):
    """Тест для проверки сервиса ImportZonesService"""
    template = Template.objects.first()
    file = File.objects.first()

    serializer_data = {
        'project': project_for_import_zones_service.id,
        'template': template.id,
        'file': file.id
    }

    process_service = ImportZonesService(serializer_data).process()

    assert process_service == 'Успешно обработано 5 строк(и).'
    assert Zone.objects.count() == 10
