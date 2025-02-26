from typing import List

from apps.helpers.services import AbstractService
from apps.promotion.models import Promotion


class UnmakeTopListPromotionService(AbstractService):
    """Сервис открепления списка акций."""

    def __init__(self, promotions_ids: List[str]):
        self.promotions_ids = promotions_ids

    def process(self):
        Promotion.objects.filter(id__in=self.promotions_ids).update(is_top=False)
