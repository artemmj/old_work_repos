import httpx
import pytest
from django.core.cache import cache

from apps.helpers.sms import API_URL

pytest_plugins = [
    'apps.faq.fixtures',
    'apps.address.fixtures',
    'apps.document.fixtures',
    'apps.user.fixtures',
    'apps.file.fixtures',
    'apps.news.fixtures',
    'apps.stories.fixtures',
    'apps.promotion.fixtures',
    'apps.departments.fixtures',
    'apps.survey.fixtures',
    'apps.regions.fixtures',
    'apps.arketa.fixtures',
]


@pytest.fixture(autouse=True)
def clear_redis():
    """Очистка кеша редис, перед и после теста."""
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def mock_200_redsms(respx_mock):
    """Мок 200 ответа апи."""
    response = httpx.Response(200)
    respx_mock.post(API_URL).mock(return_value=response)


@pytest.fixture
def mock_400_redsms(respx_mock):
    """Мок 400 ответа апи."""
    response = httpx.Response(400)
    respx_mock.post(API_URL).mock(return_value=response)
