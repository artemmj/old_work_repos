import pytest


@pytest.fixture
def phone():
    """Фикстура номера телефона."""
    return '+79270000006'


@pytest.fixture
def phone_code_key():
    return 'phone_code:{phone}'
