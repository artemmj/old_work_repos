import os

import pytest

from apps.file.models import Image
from apps.stories.models import BaseStoriesMailing
from apps.stories.services.update_is_published_stories_mailing import UpdateIsPublishedStoriesMailingService

pytestmark = [pytest.mark.django_db]


def test_update_is_published_stories_mailing(image, stories_factory, base_stories_mailing_factory):
    """Тест проверки публикации сторис рассылок."""
    picture = Image.objects.first()
    stories = stories_factory(
        count=1,
        preview=picture,
        slides=picture,
    )
    base_stories_mailing_factory(
        count=3,
        stories=stories,
        publish_datetime='2024-08-28T14:38:40.110080+0300',
        is_published=(is_published for is_published in [False, False, True])
    )
    UpdateIsPublishedStoriesMailingService().process()

    assert BaseStoriesMailing.objects.filter(is_published=False).count() == 0
    assert BaseStoriesMailing.objects.filter(is_published=True).count() == 3

    os.remove(image)
