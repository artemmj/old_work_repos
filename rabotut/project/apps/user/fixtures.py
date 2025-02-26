from typing import List, Union

import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from apps.user.models import User, UserRoles


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def master_phone():
    return '+79270000000'


@pytest.fixture
def phone():
    return '+79270000001'


@pytest.fixture
def phone2():
    return '+79270000002'


@pytest.fixture
def master_user(phone):
    return mixer.blend('user.User', phone=phone, role=UserRoles.MASTER)


@pytest.fixture
def applicant_user(phone2):
    return mixer.blend('user.User', phone=phone2, role=UserRoles.APPLICANT)


@pytest.fixture
def master_client(api_client, master_user):
    api_client.force_authenticate(user=master_user)
    return api_client


@pytest.fixture
def applicant_client(api_client, applicant_user):
    api_client.force_authenticate(user=applicant_user)
    return api_client


@pytest.fixture
def user():
    """Фикстура создания юзера."""
    return mixer.blend(
        User,
    )


@pytest.fixture
def users_factory():
    """Фикстура для создания пользователей."""

    def _factory(count: int, **fields) -> Union[User, List[User]]:
        if count == 1:
            return mixer.blend(User, **fields)
        return mixer.cycle(count).blend(User, **fields)

    return _factory
