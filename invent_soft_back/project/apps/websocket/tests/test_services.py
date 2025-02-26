import pytest

from apps.project.models import Project
from apps.websocket.services import SendWebSocketInfo

pytestmark = [pytest.mark.django_db]


def test_send_about_update_zones_with_one_zone_successful(project_for_auto_assignment: Project):
    """Тест для проверки отправки обновленной зоны по веб сокетам."""
    zone = project_for_auto_assignment.zones.first()

    request = SendWebSocketInfo().send_about_update_zones(zones=[zone])

    assert request is None


def test_send_about_update_zones_with_zones_successful(project_for_auto_assignment: Project):
    """Тест для проверки отправки обновленных зон по веб сокетам."""
    zones = project_for_auto_assignment.zones.all()

    request = SendWebSocketInfo().send_about_update_zones(zones=zones)

    assert request is None
