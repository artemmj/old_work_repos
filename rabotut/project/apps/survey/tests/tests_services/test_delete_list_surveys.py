import os

import pytest

from apps.file.models import Image
from apps.survey.models import Survey
from apps.survey.services import DeleteListSurveyService

pytestmark = [pytest.mark.django_db]


def test_delete_list_surveys(user, image, survey_factory):
    """Тест проверки удаления списка опросов."""
    preview_square = Image.objects.first()
    preview_standart = Image.objects.first()
    survey_factory(
        count=3,
        name=(name for name in ['1', '2', '3']),
        preview_square=preview_square,
        preview_standart=preview_standart,
    )
    survey_1 = Survey.objects.get(name='1')
    survey_2 = Survey.objects.get(name='2')
    survey_ids = [survey_1.id, survey_2.id]
    DeleteListSurveyService(surveys_ids=survey_ids).process()
    assert Survey.objects.non_deleted().count() == 1
