from typing import List

from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService
from apps.stories.models import Stories


class MakeTopListStoriesService(AbstractService):
    """Сервис закрепления списка сторис."""

    def __init__(self, stories_ids: List[str]):
        self.stories_ids = stories_ids

    def process(self):
        success_top_stories_count = Stories.objects.filter(is_top=True).count() + len(self.stories_ids)
        if success_top_stories_count > 7:
            raise ValidationError('Невозможно закрепить больше 7-ми сторис.')
        Stories.objects.filter(id__in=self.stories_ids).update(is_top=True)
