from typing import Dict, List

from apps.helpers.services import AbstractService
from apps.project.models import Project
from apps.terminal.models import Terminal


class BulkCreateTerminalsService(AbstractService):
    """Сервис массового создания терминалов."""

    def __init__(self, new_project: Project, terminals_content: List[Dict]):
        self.terminals_content = terminals_content
        self.new_project = new_project

    def process(self):
        Terminal.objects.bulk_create(
            [
                Terminal(
                    project=self.new_project,
                    **terminal_content,
                )
                for terminal_content in self.terminals_content
            ],
            ignore_conflicts=True,
        )
