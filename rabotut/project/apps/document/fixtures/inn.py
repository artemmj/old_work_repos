from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.document.models import Inn
from apps.document.models.status.choices import BaseUserDocumentStatuses


@pytest.fixture
def inn_factory():
    """Фикстура для генерации ИНН."""

    def _factory(count: int, **fields) -> Union[Inn, List[Inn]]:  # noqa: WPS430
        if count == 1:
            return mixer.blend(Inn, **fields)
        return mixer.cycle(count).blend(Inn, **fields)

    return _factory


@pytest.fixture
def inn_status_decline(inn_factory, applicant_user):  # noqa: WPS442
    """Фикстура ИНН со статусом отклонен."""
    inn = inn_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.DECLINE,
    )
    return inn  # noqa: WPS331


@pytest.fixture
def inn_status_approval(inn_factory, applicant_user):  # noqa: WPS442
    """Фикстура ИНН со статусом проверка."""
    inn = inn_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.APPROVAL,
    )
    return inn  # noqa: WPS331


@pytest.fixture
def inn_status_accept(inn_factory, applicant_user):  # noqa: WPS442
    """Фикстура ИНН со статусом подтвержден."""
    inn = inn_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.ACCEPT,
    )
    return inn  # noqa: WPS331
