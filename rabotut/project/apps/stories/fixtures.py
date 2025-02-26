from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.stories.models import BaseStoriesMailing, Stories, StoriesRead

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def stories_factory():
    """Фикстура для создания сторис."""

    def _factory(count: int, **fields) -> Union[Stories, List[Stories]]:
        if count == 1:
            return mixer.blend(
                Stories,
                **fields,
            )
        return mixer.cycle(count).blend(
            Stories,
            **fields,
        )

    return _factory


@pytest.fixture
def stories_read_factory():
    """Фикстура для создания прочитанных сторис."""

    def _factory(count: int, **fields) -> Union[StoriesRead, List[StoriesRead]]:
        if count == 1:
            return mixer.blend(
                StoriesRead,
                **fields,
            )
        return mixer.cycle(count).blend(
            StoriesRead,
            **fields,
        )

    return _factory


@pytest.fixture
def base_stories_mailing_factory():
    """Фикстура для создания базовой рассылки сторис."""

    def _factory(count: int, **fields) -> Union[BaseStoriesMailing, List[BaseStoriesMailing]]:
        if count == 1:
            return mixer.blend(
                BaseStoriesMailing,
                **fields,
            )
        return mixer.cycle(count).blend(
            BaseStoriesMailing,
            **fields,
        )

    return _factory
