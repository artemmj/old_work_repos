from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.document.models import Registration
from apps.document.models.status.choices import BaseUserDocumentStatuses


@pytest.fixture
def registration_factory():
    """Фикстура для генерации Страниц с регистрацией."""

    def _factory(count: int, **fields) -> Union[Registration, List[Registration]]:  # noqa: WPS430
        if count == 1:
            return mixer.blend(Registration, **fields)
        return mixer.cycle(count).blend(Registration, **fields)

    return _factory


@pytest.fixture
def registration_status_decline(registration_factory, applicant_user):  # noqa: WPS442
    """Фикстура страницы с регистрацией со статусом отклонен."""
    registration = registration_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.DECLINE,
    )
    return registration  # noqa: WPS331


@pytest.fixture
def registration_status_approval(registration_factory, applicant_user):  # noqa: WPS442
    """Фикстура страницы с регистрацией со статусом проверка."""
    registration = registration_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.APPROVAL,
    )
    return registration  # noqa: WPS331


@pytest.fixture
def registration_status_accept(registration_factory, applicant_user):  # noqa: WPS442
    """Фикстура страницы с регистрацией со статусом подтвержден."""
    registration = registration_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.ACCEPT,
    )
    return registration  # noqa: WPS331
