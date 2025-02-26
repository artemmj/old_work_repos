from apps.event.models import Event, TitleChoices
from apps.helpers.services import AbstractService
from apps.project.models import Project


class CreateEventService(AbstractService):
    """Сервис создания события."""

    def __init__(self, project: Project, title: TitleChoices, comment: str):
        self.project = project
        self.title = title
        self.comment = comment

    def process(self):
        Event.objects.create(
            project=self.project,
            title=self.title,
            comment=self.comment,
        )
