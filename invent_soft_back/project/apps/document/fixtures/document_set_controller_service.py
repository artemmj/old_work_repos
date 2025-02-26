import pytest
from mixer.backend.django import mixer

from apps.document.models import Document, DocumentStatusChoices, DocumentColorChoices
from apps.task.models import TaskTypeChoices, TaskStatusChoices, Task
from apps.zone.models import ZoneStatusChoices, Zone

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def document_set_controller_service(project):
    """Фикстура создания документа для сервиса SetDocumentControllerService."""
    zone = mixer.blend(
        Zone,
        project=project,
        serial_number=1,
        status=ZoneStatusChoices.NOT_READY,
    )
    task = mixer.blend(
        Task,
        zone=zone,
        type=TaskTypeChoices.COUNTER_SCAN,
        result=10,
        status=TaskStatusChoices.FAILED_SCAN,
    )
    document = mixer.blend(
        Document,
        serial_number=1,
        zone=zone,
        counter_scan_task=task,
        status=DocumentStatusChoices.NOT_READY,
        color=DocumentColorChoices.RED,
    )
    return document
