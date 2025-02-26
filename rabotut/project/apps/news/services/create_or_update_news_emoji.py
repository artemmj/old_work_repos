from apps.helpers.services import AbstractService
from apps.news.models import News, NewsEmoji
from apps.user.models import User


class CreateOrUpdateNewsEmojiService(AbstractService):
    """Сервис создания или обновления эмоджи."""

    def __init__(self, news: News, user: User, emoji_type: str):
        self.news = news
        self.user = user
        self.emoji_type = emoji_type

    def process(self):
        NewsEmoji.objects.update_or_create(
            news=self.news,
            user=self.user,
            defaults={
                'emoji_type': self.emoji_type,
            },
        )
