import pytest

from apps.document.models.status.choices import BaseUserDocumentStatuses

from ..services.accept_document import AcceptDocumentService


@pytest.mark.django_db
def test_accept_inn(inn_factory):
    """Тест сервиса принятия документа, ИНН."""
    inn = inn_factory(count=1)
    AcceptDocumentService(document=inn).process()
    assert inn.status == BaseUserDocumentStatuses.ACCEPT


@pytest.mark.django_db
def test_accept_passport(passport_factory):
    """Тест сервиса принятия документа, Паспорт."""
    passport = passport_factory(count=1)
    AcceptDocumentService(document=passport).process()
    assert passport.status == BaseUserDocumentStatuses.ACCEPT


@pytest.mark.django_db
def test_accept_registration(passport_factory):
    """Тест сервиса принятия документа, Регистрации."""
    registration = passport_factory(count=1)
    AcceptDocumentService(document=registration).process()
    assert registration.status == BaseUserDocumentStatuses.ACCEPT


@pytest.mark.django_db
def test_accept_selfie(passport_factory):
    """Тест сервиса принятия документа, Селфи."""
    selfie = passport_factory(count=1)
    AcceptDocumentService(document=selfie).process()
    assert selfie.status == BaseUserDocumentStatuses.ACCEPT


@pytest.mark.django_db
def test_accept_snils(passport_factory):
    """Тест сервиса принятия документа, СНИЛС."""
    snils = passport_factory(count=1)
    AcceptDocumentService(document=snils).process()
    assert snils.status == BaseUserDocumentStatuses.ACCEPT
