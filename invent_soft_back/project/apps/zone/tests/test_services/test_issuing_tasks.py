import pytest

from apps.project.models import Project
from apps.task.models import TaskTypeChoices
from apps.zone.services import IssuingTasksService

pytestmark = [pytest.mark.django_db]


def test_issuing_tasks_successful(project_for_auto_assignment: Project):
    """Тест для успешной выдачи заданий сотруднику."""
    employees = project_for_auto_assignment.employees.all()

    new_tasks = IssuingTasksService(
        zone=project_for_auto_assignment.zones.first(),
        employees=employees,
        role='counter',
    ).process()

    for employee in employees:
        assert employee.tasks.filter(id__in=new_tasks)
        assert employee.tasks.filter(id__in=new_tasks).count() == 1
        assert employee.tasks.filter(id__in=new_tasks).first().type == TaskTypeChoices.COUNTER_SCAN
