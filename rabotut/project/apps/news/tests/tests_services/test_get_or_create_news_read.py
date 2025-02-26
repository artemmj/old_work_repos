import os

import pytest

from apps.file.models import Image
from apps.news.models import NewsRead
from apps.news.services import GetOrCreateNewsReadService

pytestmark = [pytest.mark.django_db]


def test_create_news_read(user, image, news_factory):
    """Тест проверки создания прочитанной новости."""
    preview_standard = Image.objects.first()
    news = news_factory(
        count=1,
        preview_standard=preview_standard,
    )

    GetOrCreateNewsReadService(news, user).process()

    assert NewsRead.objects.count() == 1

    os.remove(image)

def test_get_news_read(user, image, news_factory, read_news_factory):
    """Тест проверки получения прочитанной новости."""
    preview_standard = Image.objects.first()
    news = news_factory(
        count=1,
        preview_standard=preview_standard,
    )
    read_news_factory(
        count=1,
        news=news,
        user=user,
    )

    GetOrCreateNewsReadService(news, user).process()

    assert NewsRead.objects.count() == 1

    os.remove(image)
