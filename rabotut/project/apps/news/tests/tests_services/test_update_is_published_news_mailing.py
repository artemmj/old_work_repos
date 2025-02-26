import os

import pytest

from apps.file.models import Image
from apps.news.models import BaseNewsMailing
from apps.news.services import UpdateIsPublishedNewsMailingService

pytestmark = [pytest.mark.django_db]


def test_update_is_published_news_mailing(image, news_factory, base_news_mailing_factory):
    """Тест проверки публикаций новостных рассылок."""
    preview_standard = Image.objects.first()
    _news = news_factory(
        count=3,
        name=(name for name in ['1', '2', '3']),
        preview_standard=preview_standard,
        is_top=True,
    )
    base_news_mailing_factory(
        count=3,
        news = (news for news in _news),
        publish_datetime= '2024-08-28T14:38:40.110080+0300',
        is_published=(is_published for is_published in [False, False, True])
    )
    UpdateIsPublishedNewsMailingService().process()

    assert BaseNewsMailing.objects.filter(is_published=False).count() == 0
    assert BaseNewsMailing.objects.filter(is_published=True).count() == 3

    os.remove(image)
