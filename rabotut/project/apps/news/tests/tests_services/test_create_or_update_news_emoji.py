import os

import pytest

from apps.file.models import Image
from apps.news.models import EmojiChoices, NewsEmoji
from apps.news.services import CreateOrUpdateNewsEmojiService

pytestmark = [pytest.mark.django_db]


def test_create_news_emoji(user, image, news_factory):
    """Тест проверки создания эмодзи новостей."""
    picture = Image.objects.first()
    news = news_factory(
        count=1,
        preview_standard=picture,
    )

    CreateOrUpdateNewsEmojiService(news=news, user=user, emoji_type='fire').process()

    assert NewsEmoji.objects.count() == 1
    assert NewsEmoji.objects.first().emoji_type == EmojiChoices.FIRE

    os.remove(image)

def test_update_news_emoji(user, image, news_factory, news_emoji_factory):
    """Тест проверки изменения эмодзи новостей."""
    preview_standard = Image.objects.first()
    news = news_factory(
        count=1,
        preview_standard=preview_standard,
    )
    news_emoji_factory(
        count=1,
        user=user,
        news=news,
        emoji_type=EmojiChoices.HEART
    )
    CreateOrUpdateNewsEmojiService(news=news, user=user, emoji_type='fire').process()

    assert NewsEmoji.objects.count() == 1
    assert NewsEmoji.objects.first().emoji_type == EmojiChoices.FIRE

    os.remove(image)
