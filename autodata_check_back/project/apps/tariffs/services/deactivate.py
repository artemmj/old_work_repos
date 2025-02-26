from typing import List

from apps.helpers.services import AbstractService
from apps.tariffs.models import Subscription


class DeactivateSubscriptionService(AbstractService):
    """Сервис деактивации подписок."""

    def process(self, subscription_ids: List):
        Subscription.objects.filter(id__in=subscription_ids).update(is_active=False)
