import os

import pytest

from apps.file.models import Image
from apps.survey.services import SendSurveyReplyService


@pytest.mark.django_db
def test_send_survey_reply(user, image, survey_factory, question_factory, option_factory):
    """Тест отправки ответа на опрос."""
    preview = Image.objects.first()

    survey = survey_factory(count=1, preview_square=preview, preview_standart=preview)
    questions = question_factory(count=3, survey=survey, number=(n for n in [1, 2, 3]))
    for question in questions:
        options = option_factory(count=3, question=question, number=(n for n in [1, 2, 3]))

    answers = [
        {
            "user": user,  # request.user - hidden field в сериалайзере
            "question": questions[0],
            "option": options[0],
        },
        {
            "user": user,
            "question": questions[1],
            "option": options[1],
        },
        {
            "user": user,
            "question": questions[2],
            "option": options[2],
        }
    ]
    SendSurveyReplyService().process(answers=answers)
