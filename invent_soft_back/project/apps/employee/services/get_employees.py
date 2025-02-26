from django.db.models import Prefetch

from apps.employee.models import Employee
from apps.helpers.services import AbstractService
from apps.task.models import Task, TaskStatusChoices


class GetEmployeesService(AbstractService):
    """Сервис для получения сотрудников"""

    def process(self, *args, **kwargs) -> Employee:
        return (
            Employee
            .objects
            .prefetch_related(
                Prefetch(
                    'tasks',
                    queryset=(
                        Task
                        .objects
                        .select_related('zone')
                        .prefetch_related('scanned_products')
                        .filter(status=TaskStatusChoices.INITIALIZED)
                    ),
                    to_attr='initialized_tasks',
                ),
            )
            .filter(is_deleted=False)
        )
