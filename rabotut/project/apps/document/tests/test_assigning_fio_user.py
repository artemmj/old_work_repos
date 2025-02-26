import pytest

from apps.document.models.status.choices import BaseUserDocumentStatuses
from apps.document.services import AssigningFioUserService

pytestmark = [pytest.mark.django_db]



def test_assigning_fio_user_service(passport_status_approval):
    """Тест для проверки сервиса присваивания ФИО из паспорта."""
    user = passport_status_approval.user

    AssigningFioUserService(passport=passport_status_approval, user=user).process()

    assert user.first_name == passport_status_approval.first_name
    assert user.last_name == passport_status_approval.last_name
    assert user.middle_name == passport_status_approval.patronymic



def test_assigning_fio_user_with_status_changed(passport_status_approval):
    """Тест для проверки присваивания ФИО из паспорта при изменении статуса."""
    user = passport_status_approval.user

    passport_status_approval.status = BaseUserDocumentStatuses.ACCEPT
    passport_status_approval.save()

    assert user.first_name == passport_status_approval.first_name
    assert user.last_name == passport_status_approval.last_name
    assert user.middle_name == passport_status_approval.patronymic
