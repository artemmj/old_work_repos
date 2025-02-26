from typing import List, Union

import pytest
from mixer.backend.django import mixer

from apps.document.models import Selfie
from apps.document.models.status.choices import BaseUserDocumentStatuses


@pytest.fixture
def selfie_factory():
    """Фикстура для генерации Селфи."""

    def _factory(count: int, **fields) -> Union[Selfie, List[Selfie]]:  # noqa: WPS430
        if count == 1:
            return mixer.blend(Selfie, **fields)
        return mixer.cycle(count).blend(Selfie, **fields)

    return _factory


@pytest.fixture
def selfie_status_decline(selfie_factory, applicant_user):  # noqa: WPS442
    """Фикстура селфи со статусом отклонен."""
    selfie = selfie_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.DECLINE,
    )
    return selfie  # noqa: WPS331


@pytest.fixture
def selfie_status_approval(selfie_factory, applicant_user):  # noqa: WPS442
    """Фикстура селфи со статусом проверка."""
    selfie = selfie_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.APPROVAL,
    )
    return selfie  # noqa: WPS331


@pytest.fixture
def selfie_status_accept(selfie_factory, applicant_user):  # noqa: WPS442
    """Фикстура селфи со статусом подтвержден."""
    selfie = selfie_factory(
        count=1,
        user=applicant_user,
        status=BaseUserDocumentStatuses.ACCEPT,
    )
    return selfie  # noqa: WPS331
