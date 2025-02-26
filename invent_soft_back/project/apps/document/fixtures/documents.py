import random
from typing import Union, List

import pytest
from mixer.backend.django import mixer

from apps.document.models import Document, DocumentColorChoices


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def documents_factory():
    """Фикстура для генерации документов."""

    def _factory(count: int, **fields) -> Union[Document, List[Document]]:
        if count == 1:
            return mixer.blend(
                Document,
                **fields,
            )
        return mixer.cycle(count).blend(
            Document,
            **fields,
        )

    return _factory


@pytest.fixture
def document_random_color():
    """Фикстура для получения случайного цвета из DocumentColorChoices."""
    return random.choice(DocumentColorChoices.choices)[0]
