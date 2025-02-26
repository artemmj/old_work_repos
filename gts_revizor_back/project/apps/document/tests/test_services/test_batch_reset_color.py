from random import randint

import pytest
from mixer.backend.django import mixer

from api.v1.document.services import BatchColorChangingService, BatchResetColorService
from apps.document.models import DocumentStatusChoices, DocumentColorChoices

pytestmark = [pytest.mark.django_db]


def test_batch_reset_color_if_color_not_changing(documents_factory):
    documents = documents_factory(
        count=3,
        color=(
            color
            for color
            in [DocumentColorChoices.WHITE, DocumentColorChoices.VIOLET, DocumentColorChoices.BLUE]
        ),
    )

    BatchResetColorService(documents=documents).process()

    assert documents[0].color == DocumentColorChoices.WHITE
    assert documents[1].color == DocumentColorChoices.VIOLET
    assert documents[2].color == DocumentColorChoices.BLUE


def test_batch_reset_color_after_changing_color_successful(documents_factory):
    documents = documents_factory(
        count=randint(5, 50),
        status=mixer.RANDOM,
    )

    document_status_color_mapping = {
        DocumentStatusChoices.NOT_READY: DocumentColorChoices.RED,
        DocumentStatusChoices.READY: DocumentColorChoices.GREEN,
    }

    BatchColorChangingService(documents=documents, color='orange').process()
    BatchResetColorService(documents=documents).process()

    for document in documents:
        document.refresh_from_db()

        assert document.prev_color is None
        assert document.color_changed == False
        assert document.color == document_status_color_mapping.get(document.status)
