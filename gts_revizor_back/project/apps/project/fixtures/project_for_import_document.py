import pytest

from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def project_for_import_document(project, zones_factory):
    zones_factory(
        count=3,
        project=project,
        title=(title for title in ['zone_1', 'zone_2', 'zone_3']),
        serial_number=(serial_number for serial_number in [1, 2, 3]),
        status=(status for status in [ZoneStatusChoices.NOT_READY, ZoneStatusChoices.NOT_READY, ZoneStatusChoices.NOT_READY]),
    )
    return project
