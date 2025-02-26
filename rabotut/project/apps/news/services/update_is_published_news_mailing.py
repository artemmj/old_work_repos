from django.utils import timezone

from apps.helpers.services import AbstractService
from apps.news.models import BaseNewsMailing


class UpdateIsPublishedNewsMailingService(AbstractService):
    """Сервис публикации новостных рассылок."""

    def process(self):
        news_mailing = BaseNewsMailing.objects.filter(publish_datetime__lte=timezone.now(), is_published=False)
        news_mailing.update(is_published=True)
