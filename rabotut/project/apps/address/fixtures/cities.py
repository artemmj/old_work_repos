from typing import List, Union

import pytest
from django.contrib.gis.geos import Point
from mixer.backend.django import mixer

from apps.address.models import City


@pytest.fixture
def cities_factory():
    """Фикстура для генерации города."""

    def _factory(count: int, **fields) -> Union[City, List[City]]:  # noqa: WPS430
        mixer.register(
            'address.City',
            location=lambda: Point(
                float(mixer.faker.latitude()),
                float(mixer.faker.longitude()),
            ),
        )

        if count == 1:
            return mixer.blend(City, **fields)
        return mixer.cycle(count).blend(City, **fields)

    return _factory
