from apps.helpers.services import AbstractService
from apps.news.models import News, NewsRead
from apps.user.models import User


class GetOrCreateNewsReadService(AbstractService):
    """Сервис создания или получения прочитанной новости."""

    def __init__(self, news: News, user: User):
        self.news = news
        self.user = user

    def process(self):
        NewsRead.objects.get_or_create(
            news=self.news,
            user=self.user,
        )
