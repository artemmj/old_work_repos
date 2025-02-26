from django.utils import timezone

from apps.helpers.services import AbstractService
from apps.survey.models import BaseSurveyMailing


class UpdateIsPublishedSurveysMailingService(AbstractService):
    """Сервис публикации опросов."""

    def process(self):
        survey_mailings = BaseSurveyMailing.objects.filter(publish_datetime__lte=timezone.now(), is_published=False)
        survey_mailings.update(is_published=True)
