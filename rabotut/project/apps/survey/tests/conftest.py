import pytest
from django.test import override_settings
from mixer.auto import mixer
from PIL import Image as Temp_image

from apps.file.models import Image
from apps.survey.models import Answer, Survey, Option, Question


@pytest.fixture
@override_settings(MEDIA_ROOT='')
def image():
    """Фикстура создания картинки."""
    image = Temp_image.new('RGB', (60, 30), color='red')
    image.save('apps/survey/tests/test.jpg')
    path_image = 'apps/survey/tests/test.jpg'

    return mixer.blend(
        Image,
        image=path_image,
    )


@pytest.fixture
def survey(image):
    return mixer.blend(Survey, preview_standart=image, preview_square=image)


@pytest.fixture
def question(survey):
    return mixer.blend(Question, survey=survey)


@pytest.fixture
def option(question):
    return mixer.blend(Option, question=question)


@pytest.fixture
def answer(question, option):
    return mixer.blend(Answer, question=question, option=option)
