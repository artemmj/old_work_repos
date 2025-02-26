from apps.document.models import Document, DocumentColorChoices, DocumentStatusChoices
from apps.task.models import TaskStatusChoices
from apps.zone.models import ZoneStatusChoices


def assert_correct_specification_changing_for(document: Document):
    """Проверяет корректность замены спецификации у переданного документа."""
    counter_scanned_products = document.counter_scan_task.scanned_products.all()
    auditor_scanned_products = document.auditor_task.scanned_products.all()

    for idx, _ in enumerate(counter_scanned_products):
        assert counter_scanned_products[idx].amount == auditor_scanned_products[idx].amount
        assert counter_scanned_products[idx].product == auditor_scanned_products[idx].product

    assert document.status == DocumentStatusChoices.READY
    assert document.color == DocumentColorChoices.GREEN
    assert document.is_replace_specification is True


def assert_change_statuses(document: Document):
    """Проверяет смены статусов документа"""
    assert document.status == DocumentStatusChoices.READY
    assert document.color == DocumentColorChoices.GREEN
    assert document.zone.status == ZoneStatusChoices.READY
    assert document.counter_scan_task.status == TaskStatusChoices.SUCCESS_SCAN
