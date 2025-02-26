from django.utils import timezone

from apps.helpers.services import AbstractService
from apps.stories.models import BaseStoriesMailing


class UpdateIsPublishedStoriesMailingService(AbstractService):
    """Сервис публикации сторис рассылок."""

    def process(self):
        stories_mailing = BaseStoriesMailing.objects.filter(publish_datetime__lte=timezone.now(), is_published=False)
        stories_mailing.update(is_published=True)
