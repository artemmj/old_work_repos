from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.regions.models import Region


@pytest.fixture
def region():
    """Фикстура создания региона."""
    return mixer.blend(Region)


@pytest.fixture
def regions_factory():
    """Фикстура для создания регионов."""

    def _factory(count: int, **fields) -> Union[Region, List[Region]]:
        if count == 1:
            return mixer.blend(Region, **fields)
        return mixer.cycle(count).blend(Region, **fields)

    return _factory
