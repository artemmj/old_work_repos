from dataclasses import dataclass
from random import randint

import pytest
from mixer.backend.django import mixer

from api.v1.document.services import BatchStatusInvertingService
from apps.document.models import DocumentStatusChoices, DocumentColorChoices
from apps.zone.models import ZoneStatusChoices

pytestmark = [pytest.mark.django_db]


@dataclass
class Document:
    status: str
    color: str
    zone_status: str


def test_batch_status_inverting_successful(documents_factory):
    """Тест для успешного инвертирования статусов документов."""
    ready_document = Document(
        status=DocumentStatusChoices.READY,
        color=DocumentColorChoices.GREEN,
        zone_status=ZoneStatusChoices.READY,
    )

    not_ready_document = Document(
        status=DocumentStatusChoices.NOT_READY,
        color=DocumentColorChoices.RED,
        zone_status=ZoneStatusChoices.NOT_READY,
    )

    document_status_mapping = {
        DocumentStatusChoices.NOT_READY: not_ready_document,
        DocumentStatusChoices.READY: ready_document,
    }

    documents = documents_factory(
        count=randint(5, 50),
        status=mixer.RANDOM,
    )

    updated_documents = BatchStatusInvertingService(documents).process()

    for document in updated_documents:
        document.refresh_from_db()

        assert document.status == document_status_mapping.get(document.status).status
        assert document.color == document_status_mapping.get(document.status).color
        assert document.zone.status == document_status_mapping.get(document.status).zone_status
