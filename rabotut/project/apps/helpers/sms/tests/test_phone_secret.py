import pytest
from django.core.cache import cache

from apps.helpers.sms.phone_secret import PhoneSecretService


@pytest.mark.django_db
def test_create_code(phone, phone_code_key):
    code = PhoneSecretService.create_code(phone)
    cached_code = cache.get(phone_code_key.format(phone=phone))
    assert cached_code == code


def test_process_creates_code(phone_code_key, phone):
    result = PhoneSecretService().process(phone)
    cached_code = cache.get(phone_code_key.format(phone=phone))

    assert cached_code is not None
    assert len(cached_code) == 6

    assert result['phone'] == phone
    assert result['code'] == cached_code
    assert result['message'] == f'Код для проверки телефона: {cached_code}'
