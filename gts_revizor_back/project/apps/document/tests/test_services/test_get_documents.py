import pytest

from api.v1.document.services import GetDocumentsForReportsService, GetDocumentsService
from apps.document.models import DocumentStatusChoices, DocumentColorChoices
from apps.employee.models import Employee
from apps.zone.models import Zone

pytestmark = [pytest.mark.django_db]


def test_get_documents_for_reports_successful(documents_inv_three_report):
    documents_filter_params = {
        'zone__project': documents_inv_three_report[0].zone.project,
        'status': DocumentStatusChoices.READY,
    }

    documents_for_reports = GetDocumentsForReportsService(documents_filter_params=documents_filter_params).process()

    assert documents_for_reports.count() == 2


def test_get_documents_successful(documents_inv_three_report):
    """Тест сервиса получения документов."""

    created_documents = GetDocumentsService().process()

    assert created_documents.count() == 3


def test_get_documents_with_filtering_successful(documents_inv_three_report):
    """Тест сервиса получения документов."""

    documents_filter_params = {
        'color': DocumentColorChoices.GREEN,
    }
    created_documents = GetDocumentsService(filter_params=documents_filter_params).process()

    assert created_documents.count() == 2
