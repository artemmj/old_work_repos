import pytest

from apps.document.models.status.choices import BaseUserDocumentStatuses

from ..services.decline_document import DeclineDocumentService


@pytest.mark.django_db
def test_decline_inn(inn_factory):
    """Тест сервиса отклонения документа, ИНН."""
    inn = inn_factory(count=1)
    DeclineDocumentService(document=inn, rejection_reason='test').process()
    assert inn.status == BaseUserDocumentStatuses.DECLINE
    assert inn.rejection_reason == 'test'


@pytest.mark.django_db
def test_decline_passport(passport_factory):
    """Тест сервиса отклонения документа, Паспорт."""
    passport = passport_factory(count=1)
    DeclineDocumentService(document=passport, rejection_reason='test').process()
    assert passport.status == BaseUserDocumentStatuses.DECLINE
    assert passport.rejection_reason == 'test'


@pytest.mark.django_db
def test_decline_registration(passport_factory):
    """Тест сервиса отклонения документа, Регистрации."""
    registration = passport_factory(count=1)
    DeclineDocumentService(document=registration, rejection_reason='test').process()
    assert registration.status == BaseUserDocumentStatuses.DECLINE
    assert registration.rejection_reason == 'test'


@pytest.mark.django_db
def test_decline_selfie(passport_factory):
    """Тест сервиса отклонения документа, Селфи."""
    selfie = passport_factory(count=1)
    DeclineDocumentService(document=selfie, rejection_reason='test').process()
    assert selfie.status == BaseUserDocumentStatuses.DECLINE
    assert selfie.rejection_reason == 'test'


@pytest.mark.django_db
def test_decline_snils(passport_factory):
    """Тест сервиса отклонения документа, СНИЛС."""
    snils = passport_factory(count=1)
    DeclineDocumentService(document=snils, rejection_reason='test').process()
    assert snils.status == BaseUserDocumentStatuses.DECLINE
    assert snils.rejection_reason == 'test'
