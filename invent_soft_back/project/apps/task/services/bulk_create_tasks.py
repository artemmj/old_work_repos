from typing import Dict, List

from apps.helpers.services import AbstractService
from apps.task.models import Task


class BulkCreateTasksService(AbstractService):
    """Сервис массового создания заданий."""

    def __init__(self, tasks_content: List[Dict]):
        self.tasks_content = tasks_content

    def process(self):
        Task.objects.bulk_create(
            [
                Task(
                    **task_content,
                )
                for task_content in self.tasks_content
            ],
            ignore_conflicts=True,
        )
