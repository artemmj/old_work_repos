import os

import pytest

from apps.file.models import Image
from apps.news.models import News
from apps.news.services import DeleteListNewsService

pytestmark = [pytest.mark.django_db]


def test_delete_list_news(user, image, news_factory):
    """Тест проверки удаления списка новостей."""
    preview_standard = Image.objects.first()
    news_factory(
        count=3,
        name=(name for name in ['1', '2', '3']),
        preview_standard=preview_standard,
        is_top=True,
    )
    news_1 = News.objects.get(name='1')
    news_2 = News.objects.get(name='2')
    news_ids = [news_1.id, news_2.id]

    DeleteListNewsService(news_ids=news_ids).process()

    assert News.objects.non_deleted().count() == 1

    os.remove(image)
