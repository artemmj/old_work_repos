import os

import pytest

from apps.file.models import Image
from apps.stories.models import StoriesRead
from apps.stories.services import GetOrCreateStoriesReadService

pytestmark = [pytest.mark.django_db]


def test_create_stories_read(user, image, stories_factory):
    """Тест проверки создания прочитанной сторис."""
    picture = Image.objects.first()
    stories = stories_factory(
        count=1,
        preview=picture,
        slides=picture,
    )

    GetOrCreateStoriesReadService(stories=stories, user=user).process()

    assert StoriesRead.objects.count() == 1

    os.remove(image)


def test_get_stories_read(user, image, stories_factory, stories_read_factory):
    """Тест проверки получения прочитанной сторис."""
    picture = Image.objects.first()
    stories = stories_factory(
        count=1,
        preview=picture,
        slides=picture,
    )
    stories_read_factory(
        count=1,
        stories=stories,
        user=user,
    )

    GetOrCreateStoriesReadService(stories=stories, user=user).process()

    assert StoriesRead.objects.count() == 1

    os.remove(image)
