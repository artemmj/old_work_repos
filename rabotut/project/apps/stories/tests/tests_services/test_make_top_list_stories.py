import os

import pytest

from apps.file.models import Image
from apps.stories.models import Stories
from apps.stories.services import MakeTopListStoriesService

pytestmark = [pytest.mark.django_db]


def test_make_top_list_stories(image, stories_factory):
    """Тест проверки закрепления списка сторис."""
    preview = Image.objects.first()
    stories_factory(
        count=3,
        name=(name for name in ['1', '2', '3']),
        is_top=False,
        preview=preview,
    )
    stories_1 = Stories.objects.get(name='1')
    stories_2 = Stories.objects.get(name='2')
    stories_ids = [stories_1.id, stories_2.id]
    MakeTopListStoriesService(stories_ids=stories_ids).process()
    assert Stories.objects.filter(is_top=True).count() == 2
    assert Stories.objects.filter(is_top=False).count() == 1
    os.remove(image)
