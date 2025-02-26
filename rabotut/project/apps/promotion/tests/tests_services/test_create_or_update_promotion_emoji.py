import os

import pytest

from apps.file.models import Image
from apps.promotion.models import EmojiChoices, PromotionEmoji
from apps.promotion.services import CreateOrUpdatePromotionEmojiService

pytestmark = [pytest.mark.django_db]


def test_create_promotion_emoji(user, image, promotion_factory):
    """Тест проверки создания эмодзи акций."""
    preview_main = Image.objects.first()
    preview_standart = Image.objects.first()
    promotion = promotion_factory(count=1, preview_main=preview_main, preview_standart=preview_standart)
    CreateOrUpdatePromotionEmojiService(promotion=promotion, user=user, emoji_type='fire').process()
    assert PromotionEmoji.objects.count() == 1
    assert PromotionEmoji.objects.first().emoji_type == EmojiChoices.FIRE
    os.remove(image)

def test_update_promotion_emoji(user, image, promotion_factory, promotion_emoji_factory):
    """Тест проверки изменения эмодзи акций."""
    preview_main = Image.objects.first()
    preview_standart = Image.objects.first()
    promotion = promotion_factory(count=1, preview_main=preview_main, preview_standart=preview_standart)
    promotion_emoji_factory(count=1, user=user, promotion=promotion, emoji_type=EmojiChoices.HEART)
    CreateOrUpdatePromotionEmojiService(promotion=promotion, user=user, emoji_type='fire').process()
    assert PromotionEmoji.objects.count() == 1
    assert PromotionEmoji.objects.first().emoji_type == EmojiChoices.FIRE
    os.remove(image)
