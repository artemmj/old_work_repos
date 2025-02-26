import os

import pytest

from apps.file.models import Image
from apps.stories.models import Stories
from apps.stories.services import UnmakeTopListStoriesService

pytestmark = [pytest.mark.django_db]


def test_unmake_top_list_stories(image, stories_factory):
    """Тест проверки открепления списка сторис."""
    preview = Image.objects.first()
    stories_factory(count=3, name=(name for name in ['1', '2', '3']), is_top=True, preview=preview)
    stories_1 = Stories.objects.get(name='1')
    stories_2 = Stories.objects.get(name='2')
    UnmakeTopListStoriesService(stories_ids=[stories_1.id, stories_2.id]).process()
    assert Stories.objects.filter(is_top=False).count() == 2
    assert Stories.objects.filter(is_top=True).count() == 1
    os.remove(image)
