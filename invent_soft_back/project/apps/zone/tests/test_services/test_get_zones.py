import pytest

from apps.project.models import Project
from apps.zone.services.get_zones import GetZonesService

pytestmark = [pytest.mark.django_db]


def test_get_zones_successful(project_for_auto_assignment: Project):
    """Тест для успешного получения списка зон в проекте."""

    zones = GetZonesService().process()

    assert zones.count() == 5
