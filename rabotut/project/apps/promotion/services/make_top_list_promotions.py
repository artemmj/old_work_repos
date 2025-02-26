from typing import List

from rest_framework.exceptions import ValidationError

from apps.helpers.services import AbstractService
from apps.promotion.models import Promotion


class MakeTopListPromotionService(AbstractService):
    """Сервис закрепления списка акций."""

    def __init__(self, promotions_ids: List[str]):
        self.promotions_ids = promotions_ids

    def process(self):
        non_deleted_top_promos = Promotion.objects.non_deleted().filter(is_top=True)
        total_top_promos_count = non_deleted_top_promos.count() + len(self.promotions_ids)
        if total_top_promos_count > 7:
            raise ValidationError('Невозможно закрепить больше 7-ми акций.')
        Promotion.objects.filter(id__in=self.promotions_ids).update(is_top=True)
