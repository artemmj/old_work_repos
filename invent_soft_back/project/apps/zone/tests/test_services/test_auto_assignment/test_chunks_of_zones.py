import pytest

from apps.zone.services.auto_assignment import AutoAssignmentZoneService

pytestmark = [pytest.mark.django_db]


def test_chunks_of_zones_successful(project, zones_factory):
    """Тест для успешного возврата последовательные части разбитого списка zones по n значений в каждом."""
    zones = zones_factory(count=9, project=project)

    chunks_of_zones = AutoAssignmentZoneService(project)._chunks_of_zones(zones, 3)

    for chunk_of_zones in chunks_of_zones:
        assert len(chunk_of_zones) == 3
