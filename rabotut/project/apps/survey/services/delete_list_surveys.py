from typing import List

from apps.helpers.services import AbstractService
from apps.survey.models import Survey


class DeleteListSurveyService(AbstractService):
    """Сервис удаления списка опросов."""

    def __init__(self, surveys_ids: List[str]):
        self.surveys_ids = surveys_ids

    def process(self):
        Survey.objects.filter(id__in=self.surveys_ids).delete()
