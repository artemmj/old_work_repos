from apps.helpers.services import AbstractService
from apps.promotion.models import Promotion, PromotionRead
from apps.user.models import User


class GetOrCreatePromotionRead(AbstractService):
    """Сервис создания или получения прочитанной акции."""

    def __init__(self, promotion: Promotion, user: User):
        self.promotion = promotion
        self.user = user

    def process(self):
        PromotionRead.objects.get_or_create(
            promotion=self.promotion,
            user=self.user,
        )
