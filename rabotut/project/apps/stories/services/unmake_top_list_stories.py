from typing import List

from apps.helpers.services import AbstractService
from apps.stories.models import Stories


class UnmakeTopListStoriesService(AbstractService):
    """Сервис открепления списка сторис."""

    def __init__(self, stories_ids: List[str]):
        self.stories_ids = stories_ids

    def process(self):
        Stories.objects.filter(id__in=self.stories_ids).update(is_top=False)
