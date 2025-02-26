from django.utils import timezone

from apps.helpers.services import AbstractService
from apps.promotion.models import BasePromotionMailing


class UpdateIsPublishedPromotionsMailingService(AbstractService):
    """Сервис публикации акций."""

    def process(self):
        news_mailing = BasePromotionMailing.objects.filter(publish_datetime__lte=timezone.now(), is_published=False)
        news_mailing.update(is_published=True)
