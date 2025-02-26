import pytest

from api.v1.document.services.change_document_status_to_not_ready import ChangeDocumentStatusToNotReady
from apps.document.models import DocumentColorChoices, DocumentStatusChoices
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


def test_change_document_status_to_not_ready_successful(documents_factory):
    """Тест для успешного изменения статуса документа на Не готов."""
    document = documents_factory(
        count=1,
        status=DocumentStatusChoices.READY,
    )

    ChangeDocumentStatusToNotReady(document).process()
    document.refresh_from_db()

    assert document.status == DocumentStatusChoices.NOT_READY
    assert document.color == DocumentColorChoices.RED
    assert document.zone.status == ZoneStatusChoices.NOT_READY
