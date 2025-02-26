from typing import List
from uuid import UUID

from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService
from apps.news.models import News


class MakeTopListNewsService(AbstractService):
    """Сервис закрепления списка новостей."""

    def __init__(self, news_ids: List[UUID]):
        self.news_ids = news_ids

    def process(self):
        total_top_news_count = News.objects.non_deleted().filter(is_top=True).count() + len(self.news_ids)
        if total_top_news_count > 7:
            raise ValidationError('Невозможно закрепить больше 7-ми новостей.')
        News.objects.filter(id__in=self.news_ids).update(is_top=True)
