import random

import pytest
from mixer.backend.django import mixer

from api.v1.document.services import BatchColorChangingService
from apps.document.models import Document

pytestmark = [pytest.mark.django_db]


def test_batch_color_changing_successful(documents_factory, document_random_color: str):
    """Тест для успешного изменения цветов документов."""
    documents_count = random.randint(2, 15)
    documents = documents_factory(
        count=documents_count,
        color=mixer.RANDOM,
    )

    BatchColorChangingService(documents=documents, color=document_random_color).process()

    updated_documents = Document.objects.filter(color=document_random_color, color_changed=True)
    assert updated_documents.count() == documents_count
