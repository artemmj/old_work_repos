from typing import List
from uuid import UUID

from apps.helpers.services import AbstractService
from apps.news.models import News


class UnmakeTopListNewsService(AbstractService):
    """Сервис открепления списка новостей."""

    def __init__(self, news_ids: List[UUID]):
        self.news_ids = news_ids

    def process(self):
        News.objects.filter(id__in=self.news_ids).update(is_top=False)
