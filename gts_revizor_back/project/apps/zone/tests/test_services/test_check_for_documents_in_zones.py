import pytest

from api.v1.zone.exceptions import ZonesNotEmptyError
from apps.project.models import Project
from apps.zone.models import Zone
from apps.zone.services.check_for_documents_in_zones import CheckForDocumentsInZonesService

pytestmark = [pytest.mark.django_db]


def test_check_for_documents_in_zones(
    project: Project,
    zones_factory,
    documents_factory,
):
    """Тест для проверки наличия документов в зонах."""
    zone_with_documents = zones_factory(
        count=1,
        project=project,
    )
    zones_factory(
        count=1,
        project=project,
    )
    documents_factory(
        count=4,
        zone=zone_with_documents,
    )
    zones = Zone.objects.all()

    with pytest.raises(ZonesNotEmptyError):
        CheckForDocumentsInZonesService(zones=zones).process()
