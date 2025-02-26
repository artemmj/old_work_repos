import pytest
from django.test import override_settings
from mixer.backend.django import mixer
from PIL import Image as Temp_image

from apps.file.models import Image


@pytest.fixture
def db_file():
    """Фикстура файла в БД."""
    return mixer.blend('file.File')


@pytest.fixture
@override_settings(MEDIA_ROOT='')
def image():
    """Фикстура создания картинки."""
    image = Temp_image.new('RGB', (60, 30), color='red')
    image.save('apps/news/tests/tests_services/test.jpg')
    path_image = 'apps/news/tests/tests_services/test.jpg'

    mixer.blend(
        Image,
        image=path_image,
    )
    return path_image
