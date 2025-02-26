from typing import List, Union

import pytest
from mixer.backend.django import mixer

from .models import Department

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def departments_factory():
    """Фикстура для создания департаметов."""

    def _factory(count: int, **fields) -> Union[Department, List[Department]]:
        if count == 1:
            return mixer.blend(Department, **fields)
        return mixer.cycle(count).blend(Department, **fields)

    return _factory
