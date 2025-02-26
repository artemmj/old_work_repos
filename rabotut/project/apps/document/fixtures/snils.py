from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.document.models import Snils
from apps.document.models.status.choices import BaseUserDocumentStatuses


@pytest.fixture
def snils_factory():
    """Фикстура для генерации СНИЛС."""

    def _factory(count: int, **fields) -> Union[Snils, List[Snils]]:  # noqa: WPS430
        if count == 1:
            return mixer.blend(Snils, **fields)
        return mixer.cycle(count).blend(Snils, **fields)

    return _factory


@pytest.fixture
def snils_status_decline(snils_factory, applicant_user):  # noqa: WPS442
    """Фикстура селфи со статусом отклонен."""
    snils = snils_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.DECLINE,
    )
    return snils  # noqa: WPS331


@pytest.fixture
def snils_status_approval(snils_factory, applicant_user):  # noqa: WPS442
    """Фикстура селфи со статусом проверка."""
    snils = snils_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.APPROVAL,
    )
    return snils  # noqa: WPS331


@pytest.fixture
def snils_status_accept(snils_factory, applicant_user):  # noqa: WPS442
    """Фикстура селфи со статусом подтвержден."""
    snils = snils_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.ACCEPT,
    )
    return snils  # noqa: WPS331
