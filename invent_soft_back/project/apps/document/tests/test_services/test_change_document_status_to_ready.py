import pytest

from api.v1.document.services.change_document_status_to_ready import ChangeDocumentStatusToReady
from apps.document.models import DocumentStatusChoices, DocumentColorChoices
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


def test_change_document_status_to_ready_successful(documents_factory):
    """Тест для успешного изменения статуса документа на Готов."""
    document = documents_factory(
        count=1,
        status=DocumentStatusChoices.NOT_READY,
    )

    ChangeDocumentStatusToReady(document).process()
    document.refresh_from_db()

    assert document.status == DocumentStatusChoices.READY
    assert document.color == DocumentColorChoices.GREEN
    assert document.zone.status == ZoneStatusChoices.READY
