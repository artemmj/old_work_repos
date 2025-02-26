import json

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_list_faq(client: APIClient, faqs_factory):
    """Тест создания и получения частых вопросов."""
    faqs_factory(count=2)

    response = client.get('/api/v1/faq/')
    response_data = json.loads(response.content)
    assert response_data['count'] == 2
    assert len(response_data['results']) == 2
