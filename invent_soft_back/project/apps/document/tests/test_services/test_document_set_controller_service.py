import pytest

from api.v1.document.services import SetDocumentControllerService
from apps.document.models import DocumentStatusChoices, DocumentColorChoices
from apps.task.models import Task
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


def test_set_controller_service_change_statuses(document_set_controller_service):
    """Тест для проверки изменении статусов при равном кол-ве результата counter_scan_task и controller_task."""
    id_task = Task.objects.first().pk
    serializer_data = {
        'task': id_task,
    }
    document = SetDocumentControllerService(document_set_controller_service, serializer_data).process()
    document.refresh_from_db()

    assert document.status == DocumentStatusChoices.READY
    assert document.zone.status == ZoneStatusChoices.READY
    assert document.color == DocumentColorChoices.GREEN
