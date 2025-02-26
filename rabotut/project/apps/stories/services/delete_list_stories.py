from typing import List
from uuid import UUID

from apps.helpers.services import AbstractService
from apps.stories.models import Stories


class DeleteListStoriesService(AbstractService):
    """Сервис удаления списка сторис."""

    def __init__(self, stories_ids: List[UUID]):
        self.stories_ids = stories_ids

    def process(self):
        Stories.objects.filter(id__in=self.stories_ids).delete()
