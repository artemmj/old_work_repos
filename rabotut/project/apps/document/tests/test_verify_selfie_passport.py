import pytest

from ..services.verify_selfie_passport import VerifySelfiePassportService


@pytest.mark.django_db
def test_success_verify_selfie_passport(mock_success_face_recognition, passport_fixture, selfie_fixture):
    """Тест сервиса обработки удачного соответствия паспорта и селфи."""
    VerifySelfiePassportService(selfie_fixture).process()
    assert selfie_fixture.recognitions
    assert selfie_fixture.recognitions.first().recognition_result['faces_is_detected']
    assert selfie_fixture.recognitions.first().recognition_result['faces_is_equal']
    assert selfie_fixture.recognitions.first().recognition_result['result']


@pytest.mark.django_db
def test_fail_verify_selfie_passport(mock_fail_face_recognition, passport_fixture, selfie_fixture):
    """Тест сервиса обработки неудачного соответствия паспорта и селфи."""
    VerifySelfiePassportService(selfie_fixture).process()
    assert selfie_fixture.recognitions
    assert not selfie_fixture.recognitions.first().recognition_result['faces_is_detected']
    assert not selfie_fixture.recognitions.first().recognition_result['faces_is_equal']
    assert not selfie_fixture.recognitions.first().recognition_result['result']
