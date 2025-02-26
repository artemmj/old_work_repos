import pytest

from api.v1.reports.services import BarcodeMatchesReportService

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'by_barcode, pair_zones, len_less_than_pairs',
    [
        (True, '3/1', 2),
        (False, '3/1', 1),
    ]
)
def test_project_barcode_and_dm_matches_report(
    project_barcode_and_dm_matches_report,
    by_barcode: bool,
    pair_zones: str,
    len_less_than_pairs: int,
):
    """
    Тест для проверки совпадения зон по ШК и ДМ и кол-во товаров.

    by_barcode: True - совпадение по Штрихкоду
    by_barcode: False - совпадение по Датаматриксу
    pair_zones: Совпадение в зонах
    len_less_than_pairs: Кол-во товаров в совпадающих зонах
    """
    payload = {
        'project': project_barcode_and_dm_matches_report.id,
        'excel': False,
        'include': 'all',
        'less_than': 1
    }
    less_than_pairs = BarcodeMatchesReportService(payload, 'http://localhost', by_barcode)._get_context()
    list_less_than_pairs = []
    for pair, _ in less_than_pairs['zones_pairs'].items():
        list_less_than_pairs.append(pair)

    assert list_less_than_pairs[0] == pair_zones
    assert len(less_than_pairs['zones_pairs'][list_less_than_pairs[0]]) == len_less_than_pairs
