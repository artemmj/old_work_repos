import pytest
from constance import config
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from apps.helpers.sms.phone_secret import PhoneSecretService


@pytest.fixture
def api_v1_send_code():
    """Фикстура api отправки кода."""
    return '/api/v1/user/mobile/send_code/'


@pytest.fixture
def api_v1_login():
    """Фикстура api логин."""
    return '/api/v1/user/mobile/login/'


@pytest.fixture
def phone():
    """Фикстура номера телефона."""
    return '+79270000000'


@pytest.fixture
def phone_2():
    """Фикстура номера телефона."""
    return '+79270000008'


@pytest.fixture
def code(phone):
    """Фикстура получения кода."""
    return PhoneSecretService().process(phone=phone)


@pytest.fixture
def code_2(phone_2):
    """Фикстура получения кода."""
    return PhoneSecretService().process(phone=phone_2)


@pytest.fixture
def user(phone):
    """Фикстура пользователя."""
    return mixer.blend('user.User', phone=phone)


@pytest.fixture
def api_client():
    """Фикстура стандартного апи клиента."""
    return APIClient()


@pytest.fixture
def sms_counter():
    """Фикстура разрешенного кол-ва смс."""
    return config.COUNT_SEND_SMS
