import pytest
from rest_framework.exceptions import ValidationError

from apps.document.models.inn.inn import Inn

from ..services import ValidateRequestUserDocumentService


@pytest.mark.django_db
def test_validate_request_user_document(users_factory, inn_factory):
    users = users_factory(count=2)
    inn_factory(
        count=2,
        value=(value for value in ['519165261949', '759008349584']),
        user=(user for user in users),
    )
    ValidateRequestUserDocumentService().process(Inn, '519165261949', users[0])
    with pytest.raises(ValidationError):
        ValidateRequestUserDocumentService().process(Inn, '519165261949', users[1])
