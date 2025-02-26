from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.document.models import Passport
from apps.document.models.status.choices import BaseUserDocumentStatuses


@pytest.fixture
def passport_factory():
    """Фикстура для генерации Паспортов."""

    def _factory(count: int, **fields) -> Union[Passport, List[Passport]]:  # noqa: WPS430
        if count == 1:
            return mixer.blend(Passport, **fields)
        return mixer.cycle(count).blend(Passport, **fields)

    return _factory


@pytest.fixture
def passport_status_approval(passport_factory, applicant_user):  # noqa: WPS442
    """Фикстура паспорта со статусом проверка."""
    passport = passport_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.APPROVAL,
        first_name='Иван',
        last_name='Иванов',
        patronymic='Иванович',
        birth_date='1995-01-01',
        date_issue='2015-10-01',
    )
    return passport  # noqa: WPS331


@pytest.fixture
def passport_status_decline(passport_factory, applicant_user):  # noqa: WPS442
    """Фикстура паспорта со статусом отклонен."""
    passport = passport_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.DECLINE,
        first_name='Иван',
        last_name='Иванов',
        patronymic='Иванович',
        birth_date='1995-01-01',
        date_issue='2015-10-01',
    )
    return passport  # noqa: WPS331


@pytest.fixture
def passport_status_accept(passport_factory, applicant_user):  # noqa: WPS442
    """Фикстура паспорта со статусом подтвержден."""
    passport = passport_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.ACCEPT,
        first_name='Иван',
        last_name='Иванов',
        patronymic='Иванович',
        birth_date='1995-01-01',
        date_issue='2015-10-01',
    )
    return passport  # noqa: WPS331
