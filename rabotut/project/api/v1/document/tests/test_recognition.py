import json

import pytest


@pytest.mark.django_db
def test_recornition_create_passport(applicant_client, db_file, mock_success_passport_recognition):
    """Тест роута распознавания."""
    response = applicant_client.post('/api/v1/document/passport/recognition/', data={'file': db_file.pk})
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    create_response = applicant_client.post('/api/v1/document/passport/', data=data)
    assert create_response.status_code == 200
