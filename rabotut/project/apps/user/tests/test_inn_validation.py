import pytest
from django.core.exceptions import ValidationError

from ..validators import InnValidator


@pytest.mark.django_db
def test_inn_validation():
    """Тест для проверки валидатора ИНН."""
    incorrect_inn_1 = '7713456564'
    incorrect_inn_2 = '123456789012'
    correct_inn = '505021556592'

    with pytest.raises(ValidationError):
        InnValidator().__call__(incorrect_inn_1)
    with pytest.raises(ValidationError):
        InnValidator().__call__(incorrect_inn_2)
    InnValidator().__call__(correct_inn)
