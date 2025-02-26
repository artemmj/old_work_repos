from django.db.models import Count, Q

from apps.employee.models import Employee
from apps.helpers.services import AbstractService
from apps.project.models import Project
from apps.task.models import TaskStatusChoices


class LeastLoadedEmployeeService(AbstractService):
    """Сервис вычисления наименее загруженного сотрудника"""

    def __init__(self, project: Project, role: str, exclude_ids: list, task_type: str):
        self.project = project
        self.role = role
        self.exclude_ids = exclude_ids or []
        self.task_type = task_type

    def process(self, *args, **kwargs) -> Employee:
        employees = self.project.employees.filter(
            roles__icontains=self.role,
            is_deleted=False,
            is_auto_assignment=True,
        ).annotate(
            active_tasks=Count(
                'tasks',
                filter=Q(tasks__status=TaskStatusChoices.INITIALIZED, tasks__type=self.task_type),
            ),
        ).order_by('active_tasks', 'serial_number')

        if self.exclude_ids:
            employees = employees.exclude(pk__in=self.exclude_ids)

        return employees.first()
