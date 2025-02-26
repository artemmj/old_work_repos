import pytest

from apps.employee.models import EmployeeRoleChoices
from apps.project.models import Project
from apps.task.models import Task
from apps.zone.services.batch_issuing_tasks import BatchIssuingTasksService

pytestmark = [pytest.mark.django_db]


def test_batch_issuing_tasks_successful(
    project: Project,
    zones_factory,
    employee_factory,
):
    """Тест для успешного пакетной выдачи заданий в зонах."""
    zones = zones_factory(
        count=5,
        project=project,
    )
    employees = employee_factory(
        count=3,
        project=project,
        roles=[EmployeeRoleChoices.COUNTER],
    )

    issuing_tasks = BatchIssuingTasksService(
        zones=zones,
        project=project,
        employees=employees,
        role='counter',
    ).process()

    created_tasks = Task.objects.all()
    assert len(issuing_tasks) == created_tasks.count()
