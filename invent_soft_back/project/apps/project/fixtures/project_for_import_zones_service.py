import pytest

from apps.template.models import TemplateFieldChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def project_for_import_zones_service(
    project,
    zones_factory,
    templates_factory,
    files_factory,
):
    """Фикстура создания проекта для проверки сервиса ImportZonesService."""
    zones_factory(
        count=5,
        project=project,
        serial_number=(serial_number for serial_number in [1, 2, 3, 4, 5]),
    )
    templates_factory(
        count=1,
        field_separator=';',
        decimal_separator=',',
        fields=[
            TemplateFieldChoices.ZONE_CODE,
            TemplateFieldChoices.ZONE_NAME,
        ]
    )
    filepath = 'apps/project/tests/test_tasks/test_import_zones/import_zones.txt'
    files_factory(count=1, file=filepath)

    return project
