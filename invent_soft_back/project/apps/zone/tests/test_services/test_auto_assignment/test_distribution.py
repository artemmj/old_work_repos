import random

import pytest

from apps.project.models import Project
from apps.zone.services.auto_assignment import AutoAssignmentZoneService

pytestmark = [pytest.mark.django_db]


def test_distribution_successful(project_for_auto_assignment: Project):
    """Тест для успешного распределения сотрудников по зонам."""
    auto_zones_amount = random.randint(1, 4)
    project_for_auto_assignment.rmm_settings.auto_zones_amount = auto_zones_amount
    project_for_auto_assignment.rmm_settings.save()
    project_for_auto_assignment.refresh_from_db()

    zone_assignment = AutoAssignmentZoneService(project_for_auto_assignment)._distribution(
        zones=project_for_auto_assignment.zones.all(),
        employees=project_for_auto_assignment.employees.all(),
        auto_zones_amount=auto_zones_amount,
    )
    employee_with_zones = project_for_auto_assignment.employees.first()

    assert project_for_auto_assignment.rmm_settings.auto_zones_amount == auto_zones_amount
    assert (len(zone_assignment[0].get(employee_with_zones))) == auto_zones_amount
