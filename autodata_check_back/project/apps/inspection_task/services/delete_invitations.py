from django.contrib.auth import get_user_model

from apps.helpers.services import AbstractService
from apps.inspection_task.models.task import InspectionTask

User = get_user_model()


class DeleteInvitationsService(AbstractService):
    """Сервис удаления приглашений по заданиям."""

    def __init__(self, task: InspectionTask, inspector: User = None):  # noqa: D107
        self.task = task
        self.inspector = inspector

    def process(self, *args, **kwargs):
        invitations = self.task.invitations.all()
        if self.inspector:
            invitations = invitations.exclude(inspector=self.inspector)
        invitations.delete()
