import pytest

from api.v1.reports.services import InvInZonesReportService

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'serial_number_start, serial_number_end, number_of_zones',
    [
        (1, 3, 2),
        (1, 2, 1),
    ],
)
def test_inv_in_zones_report_numbers_of_zones(
    project_inv_in_zones_report,
    serial_number_start: int,
    serial_number_end: int,
    number_of_zones: int,
):
    """
    Тест для проверки кол-во зон входящих в отчет Общее кол-во ТМЦ по зонам.

    serial_number_start - начало порядкого номера
    serial_number_end - конец порядкого номера
    number_of_zones - кол-во зон попавшие в отчет
    """
    payload = {
        'project': project_inv_in_zones_report.id,
        'excel': False,
        'serial_number_start': serial_number_start,
        'serial_number_end': serial_number_end,
    }

    context = InvInZonesReportService(payload, 'http://localhost')._create_context()

    assert len(context['zones']) == number_of_zones
