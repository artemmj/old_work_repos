import pytest

from apps.project.models import Project
from apps.zone.services.auto_assignment import AutoAssignmentZoneService

pytestmark = [pytest.mark.django_db]


def test_calculation_employees_successful(project_for_auto_assignment: Project):
    """Тест для успешного вычисления подходящих сотрудников для авто-назначения."""
    suitable_employees_for_auto_assignment = AutoAssignmentZoneService(
        project_for_auto_assignment,
    )._calculation_employees()

    assert suitable_employees_for_auto_assignment.count() == 3
    assert suitable_employees_for_auto_assignment[0].serial_number == 3
