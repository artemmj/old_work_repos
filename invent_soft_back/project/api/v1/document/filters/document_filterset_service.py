import logging
from datetime import datetime

from django.db.models import IntegerField
from django.db.models.functions import Cast

from api.v1.document.services import CheckAuditorDiscrepancyService
from apps.document.models import Document, DocumentStatusChoices

logger = logging.getLogger('django')


class DocumentFilterSetService:  # noqa: WPS338 WPS214
    """Класс оболочка для фильтров вкладки Документы."""

    def project_method(self, queryset, name, value):
        if value:
            return queryset.filter(zone__project=value)
        return queryset

    def vendor_code_filter(self, queryset, name, value):
        if not value:
            return queryset

        docs_pks = Document.objects.filter(
            counter_scan_task__result__gt=0,
            counter_scan_task__scanned_products__product__vendor_code=value,
        ).values_list('pk', flat=True)

        return queryset.filter(pk__in=docs_pks)

    def barcode_filter(self, queryset, name, value):
        if not value:
            return queryset

        docs_pks = Document.objects.filter(
            counter_scan_task__result__gt=0,
            counter_scan_task__scanned_products__product__barcode=value,
        ).values_list('pk', flat=True)

        return queryset.filter(pk__in=docs_pks)

    def product_title_filter(self, queryset, name, value):
        if not value:
            return queryset

        docs_pks = Document.objects.filter(
            counter_scan_task__result__gt=0,
            counter_scan_task__scanned_products__product__title=value,
        ).values_list('pk', flat=True)

        return queryset.filter(pk__in=docs_pks)

    def start_audit_date_meth(self, queryset, name, value):
        if not value and value is not False:
            return queryset
        return queryset.filter(start_audit_date__gte=datetime.strptime(value, '%Y-%m-%dT%H:%M'))

    def end_audit_date_meth(self, queryset, name, value):
        if not value and value is not False:
            return queryset
        return queryset.filter(end_audit_date__lte=datetime.strptime(value, '%Y-%m-%dT%H:%M'))

    def suspicious_meth(self, queryset, name, value):
        if not value and value is not False:
            return queryset
        return queryset.filter(suspicious=value)

    def status_meth(self, queryset, name, value):
        if not value and value is not False:
            return queryset

        if value is True:
            return queryset.filter(status=DocumentStatusChoices.READY)
        elif value is False:
            return queryset.filter(status=DocumentStatusChoices.NOT_READY)

    def zone_code_start_gte(self, queryset, name, value):
        if not value and value is not False:
            return queryset
        return queryset.filter(zone__serial_number__gte=value)

    def zone_code_end_lte(self, queryset, name, value):
        if not value and value is not False:
            return queryset
        return queryset.filter(zone__serial_number__lte=value)

    # fake id

    def fake_id_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(fake_id=value)

    def fake_id_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(fake_id=value)

    def fake_id_more_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(fake_id__gte=value)

    def fake_id_less_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(fake_id__lte=value)

    # zone number (code)

    def zone_number_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(zone__code=value)

    def zone_number_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(zone__code=value)

    def zone_number_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(zone__code__contains=value)

    def zone_number_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(zone__code__contains=value)

    # zone_title

    def zone_title_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(zone__title=value)

    def zone_title_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(zone__title=value)

    def zone_title_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(zone__title__contains=value)

    def zone_title_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(zone__title__contains=value)

    # counter scan

    def counter_scan_barcode_amount_eq_meth(self, queryset, name, value):
        return queryset.filter(counter_scan_barcode_amount=value)

    def counter_scan_not_eq_meth(self, queryset, name, value):
        return queryset.exclude(counter_scan_barcode_amount=value)

    def counter_scan_more_than_meth(self, queryset, name, value):
        return queryset.filter(counter_scan_barcode_amount__gte=value)

    def counter_scan_less_than_meth(self, queryset, name, value):
        if value == 0:
            return queryset.filter(counter_scan_barcode_amount=value)
        return queryset.filter(counter_scan_barcode_amount__lte=value)

    def controller_eq_meth(self, queryset, name, value):
        return queryset.filter(controller_barcode_amount=value)

    def controller_not_eq_meth(self, queryset, name, value):
        return queryset.exclude(controller_barcode_amount=value)

    def controller_more_than_meth(self, queryset, name, value):
        return queryset.filter(controller_barcode_amount__gte=value)

    def controller_less_than_meth(self, queryset, name, value):
        if value == 0:
            return queryset.filter(controller_barcode_amount=value)
        return queryset.filter(controller_barcode_amount__lte=value)

    # auditor scan

    def auditor_eq_meth(self, queryset, name, value):
        return queryset.filter(auditor_task__result=value)

    def auditor_not_eq_meth(self, queryset, name, value):
        return queryset.exclude(auditor_task__result=value).exclude(auditor_task__result__isnull=True)

    def auditor_more_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(auditor_task__result__gte=value)

    def auditor_less_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(auditor_task__result__lte=value)

    def auditor_task_result_contains_meth(self, queryset, name, value):
        return (
            queryset
            .annotate(auditor_task_result_int=Cast('auditor_task__result', output_field=IntegerField()))
            .filter(auditor_task_result_int__contains=value)
        )

    def auditor_task_result_not_contains_meth(self, queryset, name, value):
        return (
            queryset
            .annotate(auditor_task_result_int=Cast('auditor_task__result', output_field=IntegerField()))
            .exclude(auditor_task_result_int__contains=value)
            .exclude(auditor_task__result__isnull=True)
        )

    def auditor_task_result_discrepancy_meth(self, queryset, name, value):  # noqa: WPS231
        documents_with_discrepancy = []
        documents_without_discrepancy = []

        for document in queryset:
            if document.counter_scan_task and document.auditor_task:
                is_auditor_discrepancy = CheckAuditorDiscrepancyService().process(
                    document.counter_scan_task,
                    document.auditor_task,
                )
                if is_auditor_discrepancy:
                    documents_with_discrepancy.append(document.pk)
                if not is_auditor_discrepancy:
                    documents_without_discrepancy.append(document.pk)
        if value:
            return queryset.filter(pk__in=documents_with_discrepancy)
        if not value:
            return queryset.filter(pk__in=documents_without_discrepancy)

    # auditor controller

    def auditor_controller_eq_meth(self, queryset, name, value):
        return queryset.filter(auditor_controller_task__result=value)

    def auditor_controller_not_eq_meth(self, queryset, name, value):
        return (
            queryset
            .exclude(auditor_controller_task__result=value)
            .exclude(auditor_controller_task__result__isnull=True)
        )

    def auditor_controller_more_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(auditor_controller_task__result__gte=value)

    def auditor_controller_less_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(auditor_controller_task__result__lte=value)

    def auditor_controller_task_result_contains_meth(self, queryset, name, value):
        return (
            queryset
            .annotate(
                auditor_controller_task_result_int=Cast(
                    'auditor_controller_task__result',
                    output_field=IntegerField(),
                ),
            )
            .filter(auditor_controller_task_result_int__contains=value)
        )

    def auditor_controller_task_result_not_contains_meth(self, queryset, name, value):  # noqa: WPS118
        return (
            queryset
            .annotate(
                auditor_controller_task_result_int=Cast(
                    'auditor_controller_task__result',
                    output_field=IntegerField(),
                ),
            )
            .exclude(auditor_controller_task_result_int__contains=value)
            .exclude(auditor_controller_task__result__isnull=True)
        )

    def auditor_controller_task_result_discrepancy_meth(self, queryset, name, value):  # noqa: WPS231 WPS118
        documents_with_discrepancy = []
        documents_without_discrepancy = []
        for document in queryset:
            if document.controller_task and document.auditor_controller_task:
                if document.controller_task.result != document.auditor_controller_task.result:
                    documents_with_discrepancy.append(document.pk)
                if document.controller_task.result == document.auditor_controller_task.result:
                    documents_without_discrepancy.append(document.pk)
        if value:
            return queryset.filter(pk__in=documents_with_discrepancy)
        if not value:
            return queryset.filter(pk__in=documents_without_discrepancy)

    # auditor external

    def auditor_external_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(auditor_external_task__result=value)

    def auditor_external_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(auditor_external_task__result=value)

    def auditor_external_more_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(auditor_external_task__result__gte=value)

    def auditor_external_less_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(auditor_external_task__result__lte=value)

    # storage

    def storage_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(storage_task__result=value)

    def storage_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(storage_task__result__gte=value)

    def storage_more_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(storage_task__result__gte=value)

    def storage_less_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(storage_task__result__lte=value)

    # tsd number

    def tsd_number_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(tsd_number=value)

    def tsd_number_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(tsd_number=value)

    def tsd_number_less_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(tsd_number__lte=value)

    def tsd_number_more_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(tsd_number__gte=value)

    # employee serial number

    def employee__serial_number_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(employee__serial_number=value)

    def employee__serial_number_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(employee__serial_number=value)

    def employee__serial_number_more_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(employee__serial_number__gte=value)

    def employee__serial_number_less_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(employee__serial_number__lte=value)

    # employee

    def employee_name_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(employee__username=value)

    def employee_name_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(employee__username=value)

    def employee_name_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(employee__username__contains=value)

    def employee_name_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(employee__username__contains=value)
