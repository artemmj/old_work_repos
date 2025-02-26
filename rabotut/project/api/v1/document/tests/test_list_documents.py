import pytest

from apps.document.models.status.choices import BaseUserDocumentStatuses as doc_stats


@pytest.mark.django_db
def test_list_inn(master_client, inn_factory):
    """Тест фильтрации списка ИНН по query_params."""
    inn_factory(
        count=3,
        value=(value for value in ['519165261949', '759008349584', '060228780081']),
        status=(status for status in [doc_stats.APPROVAL, doc_stats.ACCEPT, doc_stats.DECLINE]),
    )
    response = master_client.get('/api/v1/document/inn/?status=approval')
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['status']['value'] == doc_stats.APPROVAL


@pytest.mark.django_db
def test_list_passport(master_client, passport_factory):
    """Тест фильтрации списка Паспортов по query_params."""
    passport_factory(
        count=3,
        status=(status for status in [doc_stats.APPROVAL, doc_stats.ACCEPT, doc_stats.DECLINE]),
    )
    response = master_client.get('/api/v1/document/passport/?status=approval')
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['status']['value'] == doc_stats.APPROVAL


@pytest.mark.django_db
def test_list_registartion(master_client, registration_factory):
    """Тест фильтрации списка Страниц с регистрацией по query_params."""
    registration_factory(
        count=3,
        status=(status for status in [doc_stats.APPROVAL, doc_stats.ACCEPT, doc_stats.DECLINE]),
    )
    response = master_client.get('/api/v1/document/registration/?status=approval')
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['status']['value'] == doc_stats.APPROVAL


@pytest.mark.django_db
def test_list_selfie(master_client, selfie_factory):
    """Тест фильтрации списка Паспортов по query_params."""
    selfie_factory(
        count=3,
        status=(status for status in [doc_stats.APPROVAL, doc_stats.ACCEPT, doc_stats.DECLINE]),
    )
    response = master_client.get('/api/v1/document/selfie/?status=approval')
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['status']['value'] == doc_stats.APPROVAL


@pytest.mark.django_db
def test_list_snils(master_client, snils_factory):
    """Тест фильтрации списка СНИЛС по query_params."""
    snils_factory(
        count=3,
        status=(status for status in [doc_stats.APPROVAL, doc_stats.ACCEPT, doc_stats.DECLINE]),
    )
    response = master_client.get('/api/v1/document/snils/?status=approval')
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['results'][0]['status']['value'] == doc_stats.APPROVAL
