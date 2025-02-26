from dataclasses import asdict

import pytest

from ..services.face_matching_recognition import FaceMatchingRecognition


@pytest.mark.django_db
def test_success_face_matching_recognition(mock_success_face_recognition, db_file):
    """Тест сервиса совпадения фото паспорта и селфи."""
    result = asdict(FaceMatchingRecognition(image=db_file).process())
    assert result.get('faces_is_equal')
    assert result.get('result')


@pytest.mark.django_db
def test_failed_face_matching_recognition(mock_fail_face_recognition, db_file):
    """Тест сервиса совпадения фото паспорта и селфи."""
    result = asdict(FaceMatchingRecognition(image=db_file).process())
    assert not result.get('faces_is_equal')
    assert not result.get('result')
    assert result.get('error') == 'Error'
