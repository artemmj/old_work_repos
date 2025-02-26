import pytest

from apps.document.services.passport_recognition import PassportRecognitionError, PassportRecognitionService


@pytest.mark.django_db
def test_success_passport_recognition(mock_success_passport_recognition, passport_fixture, selfie_fixture, db_file):
    """Тест удачного результата сервиса обработки соответствия паспорта и селфи."""
    service_result = PassportRecognitionService(db_file).process()
    assert 'first_name' in service_result
    assert service_result['first_name'] == 'Влас'


@pytest.mark.django_db
def test_fail_passport_recognition(mock_fail_passport_recognition, passport_fixture, selfie_fixture, db_file):
    """Тест неудачного результата сервиса обработки соответствия паспорта и селфи."""
    with pytest.raises(PassportRecognitionError):
        PassportRecognitionService(db_file).process()
