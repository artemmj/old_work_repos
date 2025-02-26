from typing import Dict, List

from apps.event.models import Event
from apps.helpers.services import AbstractService
from apps.project.models import Project


class BulkCreateEventsService(AbstractService):
    """Сервис массового создания событий."""

    def __init__(self, new_project: Project, events_content: List[Dict]):
        self.events_content = events_content
        self.new_project = new_project

    def process(self):
        Event.objects.bulk_create(
            [
                Event(
                    project=self.new_project,
                    **event_content,
                )
                for event_content in self.events_content
            ],
            ignore_conflicts=True,
        )
