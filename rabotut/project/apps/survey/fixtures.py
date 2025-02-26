from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.survey.models import Answer, Option, Question, Survey

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def survey_factory():
    """Фикстура для создания опросов."""
    def _factory(count: int, **fields) -> Union[Survey, List[Survey]]:
        if count == 1:
            return mixer.blend(Survey, **fields)
        return mixer.cycle(count).blend(Survey, **fields)
    return _factory


@pytest.fixture
def question_factory():
    """Фикстура для создания вопросов."""
    def _factory(count: int, **fields) -> Union[Question, List[Question]]:
        if count == 1:
            return mixer.blend(Question, **fields)
        return mixer.cycle(count).blend(Question, **fields)
    return _factory


@pytest.fixture
def answer_factory():
    """Фикстура для создания ответов."""
    def _factory(count: int, **fields) -> Union[Answer, List[Answer]]:
        if count == 1:
            return mixer.blend(Answer, **fields)
        return mixer.cycle(count).blend(Answer, **fields)
    return _factory


@pytest.fixture
def option_factory():
    """Фикстура для создания вариантов ответов."""
    def _factory(count: int, **fields) -> Union[Option, List[Option]]:
        if count == 1:
            return mixer.blend(Option, **fields)
        return mixer.cycle(count).blend(Option, **fields)
    return _factory
