from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.faq.models import Faq


@pytest.fixture
def faqs_factory():
    """Фикстура для генерации частого вопроса."""

    def _factory(count: int, **fields) -> Union[Faq, List[Faq]]:  # noqa: WPS430
        if count == 1:
            return mixer.blend(Faq, **fields)
        return mixer.cycle(count).blend(Faq, **fields)

    return _factory
