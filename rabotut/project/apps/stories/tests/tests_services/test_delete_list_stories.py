import os

import pytest

from apps.file.models import Image
from apps.stories.models import Stories
from apps.stories.services import DeleteListStoriesService

pytestmark = [pytest.mark.django_db]


def test_delete_list_stories(image, stories_factory):
    """Тест проверки удаления списка сторис."""
    picture = Image.objects.first()
    stories_factory(
        count=3,
        name=(name for name in ['1', '2', '3']),
        preview=picture,
        slides=picture,
    )
    stories_1 = Stories.objects.get(name='1')
    stories_2 = Stories.objects.get(name='2')
    stories_ids = [stories_1.id, stories_2.id]

    DeleteListStoriesService(stories_ids=stories_ids).process()

    assert Stories.objects.non_deleted().count() == 1

    os.remove(image)
