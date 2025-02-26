import pytest

from apps.project.models import Project
from apps.zone.services.auto_assignment import AutoAssignmentZoneService

pytestmark = [pytest.mark.django_db]


def test_calculation_zones_successful(
    project_for_auto_assignment: Project,
):
    """Тест для успешного вычисления подходящих зон для авто-назначения."""
    suitable_zones_for_auto_assignment = AutoAssignmentZoneService(project_for_auto_assignment)._calculation_zones()

    assert suitable_zones_for_auto_assignment.count() == 3
