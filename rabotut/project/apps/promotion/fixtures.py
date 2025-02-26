from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.promotion.models import BasePromotionMailing, Promotion, PromotionEmoji, PromotionRead

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def promotion_factory():
    """Фикстура для создания акций."""
    def _factory(count: int, **fields) -> Union[Promotion, List[Promotion]]:
        if count == 1:
            return mixer.blend(Promotion, **fields)
        return mixer.cycle(count).blend(Promotion, **fields)
    return _factory


@pytest.fixture
def read_promotion_factory():
    """Фикстура для создания прочитанных акций."""
    def _factory(count: int, **fields) -> Union[PromotionRead, List[PromotionRead]]:
        if count == 1:
            return mixer.blend(PromotionRead, **fields)
        return mixer.cycle(count).blend(PromotionRead, **fields)
    return _factory


@pytest.fixture
def promotion_emoji_factory():
    """Фикстура для создания эмодзи акций."""
    def _factory(count: int, **fields) -> Union[PromotionEmoji, List[PromotionEmoji]]:
        if count == 1:
            return mixer.blend(PromotionEmoji, **fields)
        return mixer.cycle(count).blend(PromotionEmoji, **fields)
    return _factory


@pytest.fixture
def base_promotion_mailing_factory():
    """Фикстура для создания базовой рассылки акций."""
    def _factory(count: int, **fields) -> Union[BasePromotionMailing, List[BasePromotionMailing]]:
        if count == 1:
            return mixer.blend(BasePromotionMailing, **fields)
        return mixer.cycle(count).blend(BasePromotionMailing, **fields)
    return _factory
