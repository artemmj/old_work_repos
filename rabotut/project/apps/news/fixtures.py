from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.news.models import BaseNewsMailing, News, NewsEmoji, NewsRead

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def news_factory():
    """Фикстура для создания новостей."""

    def _factory(count: int, **fields) -> Union[News, List[News]]:
        if count == 1:
            return mixer.blend(
                News,
                **fields,
            )
        return mixer.cycle(count).blend(
            News,
            **fields,
        )

    return _factory


@pytest.fixture
def read_news_factory():
    """Фикстура для создания прочитанных новостей."""

    def _factory(count: int, **fields) -> Union[News, List[News]]:
        if count == 1:
            return mixer.blend(
                NewsRead,
                **fields,
            )
        return mixer.cycle(count).blend(
            NewsRead,
            **fields,
        )

    return _factory


@pytest.fixture
def news_emoji_factory():
    """Фикстура для создания эмодзи новостей."""

    def _factory(count: int, **fields) -> Union[NewsEmoji, List[NewsEmoji]]:
        if count == 1:
            return mixer.blend(
                NewsEmoji,
                **fields,
            )
        return mixer.cycle(count).blend(
            NewsEmoji,
            **fields,
        )

    return _factory


@pytest.fixture
def base_news_mailing_factory():
    """Фикстура для создания базовой рассылки новостей."""

    def _factory(count: int, **fields) -> Union[BaseNewsMailing, List[BaseNewsMailing]]:
        if count == 1:
            return mixer.blend(
                BaseNewsMailing,
                **fields,
            )
        return mixer.cycle(count).blend(
            BaseNewsMailing,
            **fields,
        )

    return _factory
