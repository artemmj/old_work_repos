import pytest

from api.v1.reports.services.inventory_in_zones_in_zones_report import InventoryInZonesInZonesReportService

pytestmark = [pytest.mark.django_db]


def test_inventory_in_zones_report(zones_for_inventory_in_zones_report):
    """Тест для проверки общего кол-ва товаров в готовых зонах."""
    payload = {
        'project': zones_for_inventory_in_zones_report[0].project.id,
        'document_type': 'pdf',
        'group_by': 'barcode',
        'zones': [],
    }

    clear_context = InventoryInZonesInZonesReportService(payload, 'http://localhost')._create_context()

    assert clear_context['zones'][zones_for_inventory_in_zones_report[0].serial_number]['total'] == 20
    assert clear_context['zones'][zones_for_inventory_in_zones_report[-1].serial_number]['total'] == 25


def test_inventory_in_zones_report_add_art_in_vendor_code(zones_for_inventory_in_zones_report):
    """Тест для проверки прибавления префикса art_ в vendor_code при его отсуствии."""
    payload = {
        'project': zones_for_inventory_in_zones_report[0].project.id,
        'document_type': 'pdf',
        'group_by': 'barcode',
        'zones': [],
    }

    clear_context = InventoryInZonesInZonesReportService(payload, 'http://localhost')._create_context()

    assert (
        clear_context['zones'][zones_for_inventory_in_zones_report[0].serial_number]['products'][0]['vendor_code'].
        startswith('art_')) is False
    assert (
        clear_context['zones'][zones_for_inventory_in_zones_report[-1].serial_number]['products'][0]['vendor_code'].
        startswith('art_'),
    )


def test_inventory_in_zones_report_zone_status_not_ready(zones_for_inventory_in_zones_report):
    """Тест для проверки отсуствия зоны в отчете , т.к она в статусе NOT_READY."""
    payload = {
        'project': zones_for_inventory_in_zones_report[0].project.id,
        'document_type': 'pdf',
        'group_by': 'barcode',
        'zones': [],
    }

    clear_context = InventoryInZonesInZonesReportService(payload, 'http://localhost')._create_context()

    with pytest.raises(KeyError):
        clear_context['zones'][zones_for_inventory_in_zones_report[1].serial_number]
