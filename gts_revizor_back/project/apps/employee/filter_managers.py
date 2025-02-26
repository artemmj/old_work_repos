from django.db.models import Prefetch, QuerySet

from apps.task.models import Task, TaskStatusChoices


class EmployeeFilterManager:

    def get_employee(self, queryset: QuerySet) -> QuerySet:
        """Получение сотрудников с заданиями в статусе инициализированы для работы."""
        return (
            queryset
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
            .order_by('serial_number')
        )
