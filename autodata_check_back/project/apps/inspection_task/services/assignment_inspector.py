from django.db import transaction

from apps.helpers.services import AbstractService
from apps.inspection_task.models.invitation import Invitation
from apps.inspection_task.models.task import InspectionTask, InspectorTaskStatuses


class AssignmentInspectorService(AbstractService):
    """Сервис назначения инспектора на задание."""

    @transaction.atomic()
    def process(self, invitation: Invitation):
        for task in InspectionTask.objects.filter(   # noqa: WPS352
            id=invitation.task_id,
        ).select_for_update(of=('self',), skip_locked=True):
            task.inspector = invitation.inspector
            task.status = InspectorTaskStatuses.TASK_ACCEPTED
            task.save()
