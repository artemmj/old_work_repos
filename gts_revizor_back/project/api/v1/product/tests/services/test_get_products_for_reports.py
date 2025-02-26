import pytest

from api.v1.product.services import GetProductsForReportsService

pytestmark = [pytest.mark.django_db]


def test_get_products_for_reports_successful(documents_inv_three_report):
    products_for_reports = GetProductsForReportsService(project=documents_inv_three_report[0].zone.project).process()

    assert products_for_reports.count() == 10
