from apps.helpers.services import AbstractService
from apps.stories.models import Stories, StoriesRead
from apps.user.models import User


class GetOrCreateStoriesReadService(AbstractService):
    """Сервис создания или получения прочитанной сторис."""

    def __init__(self, stories: Stories, user: User):
        self.stories = stories
        self.user = user

    def process(self):
        StoriesRead.objects.get_or_create(
            stories=self.stories,
            user=self.user,
        )
