from apps.helpers.services import AbstractService
from apps.promotion.models import Promotion, PromotionEmoji
from apps.user.models import User


class CreateOrUpdatePromotionEmojiService(AbstractService):
    """Сервис создания или обновления реакции эмодзи."""

    def __init__(self, promotion: Promotion, user: User, emoji_type: str):
        self.promotion = promotion
        self.user = user
        self.emoji_type = emoji_type

    def process(self):
        PromotionEmoji.objects.update_or_create(
            promotion=self.promotion,
            user=self.user,
            defaults={
                'emoji_type': self.emoji_type,
            },
        )
