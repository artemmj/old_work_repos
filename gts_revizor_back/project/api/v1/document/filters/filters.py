from django_filters import BooleanFilter, CharFilter, FilterSet, NumberFilter

from apps.document.models import Document, DocumentStatusChoices
from apps.helpers.filters import CharInFilter
from apps.product.models import ScannedProduct

from .document_filterset_service import DocumentFilterSetService


class DocumentFilterSet(FilterSet):  # noqa: WPS214
    zone_serial_start = NumberFilter(field_name='zone__serial_number', lookup_expr='gte')
    zone_serial_end = NumberFilter(field_name='zone__serial_number', lookup_expr='lte')

    project = CharFilter(field_name='zone__project', method='project_method')

    zone_code_start = CharFilter(field_name='code', method='zone_code_start_gte')
    zone_code_end = CharFilter(field_name='code', method='zone_code_end_lte')

    product_title = CharFilter(method='product_title_filter')
    barcode = CharFilter(method='barcode_filter')
    vendor_code = CharFilter(method='vendor_code_filter')

    start_audit_date = CharFilter(method='start_audit_date_meth')
    end_audit_date = CharFilter(method='end_audit_date_meth')

    suspicious = BooleanFilter(field_name='suspicious', method='suspicious_meth')
    status = BooleanFilter(field_name='status', method='status_meth')

    id_eq = NumberFilter(field_name='fake_id', method='fake_id_eq_meth')
    id_not_eq = NumberFilter(field_name='fake_id', method='fake_id_not_eq_meth')
    id_more_than = NumberFilter(field_name='fake_id', method='fake_id_more_than_meth')
    id_less_than = NumberFilter(field_name='fake_id', method='fake_id_less_than_meth')

    # NOTE Тут под капотом фильтруется по коду зоны а не по серийному номеру, так нужно
    zone__serial_number_eq = NumberFilter(field_name='zone__serial_number', method='zone_number_eq_meth')
    zone__serial_number_not_eq = NumberFilter(field_name='zone__serial_number', method='zone_number_not_eq_meth')
    zone__serial_number_contains = NumberFilter(field_name='zone__serial_number', method='zone_number_contains_meth')
    zone__serial_number_not_contains = NumberFilter(
        field_name='zone__serial_number',
        method='zone_number_not_contains_meth',
    )

    zone_title_eq = CharFilter(field_name='zone__title', method='zone_title_eq_meth')
    zone_title_not_eq = CharFilter(field_name='zone__title', method='zone_title_not_eq_meth')
    zone_title_contains = CharFilter(field_name='zone__title', method='zone_title_contains_meth')
    zone_title_not_contains = CharFilter(field_name='zone__title', method='zone_title_not_contains_meth')

    counter_scan_task__result_eq = NumberFilter(method='counter_scan_eq_meth')
    counter_scan_task__result_not_eq = NumberFilter(method='counter_scan_not_eq_meth')
    counter_scan_task__result_more_than = NumberFilter(method='counter_scan_more_than_meth')
    counter_scan_task__result_less_than = NumberFilter(method='counter_scan_less_than_meth')

    controller_task__result_eq = NumberFilter(method='controller_eq_meth')
    controller_task__result_not_eq = NumberFilter(method='controller_not_eq_meth')
    controller_task__result_more_than = NumberFilter(method='controller_more_than_meth')
    controller_task__result_less_than = NumberFilter(method='controller_less_than_meth')

    auditor_task__result_eq = NumberFilter(method='auditor_eq_meth')
    auditor_task__result_not_eq = NumberFilter(method='auditor_not_eq_meth')
    auditor_task__result_more_than = NumberFilter(method='auditor_more_than_meth')
    auditor_task__result_less_than = NumberFilter(method='auditor_less_than_meth')
    auditor_task__result_contains = NumberFilter(
        field_name='auditor_task__result',
        method='auditor_task_result_contains_meth',
    )
    auditor_task__result_not_contains = NumberFilter(
        field_name='auditor_task__result',
        method='auditor_task_result_not_contains_meth',
    )
    auditor_task__result__discrepancy = BooleanFilter(method='auditor_task_result_discrepancy_meth')

    auditor_controller_task__result_eq = NumberFilter(method='auditor_controller_eq_meth')
    auditor_controller_task__result_not_eq = NumberFilter(method='auditor_controller_not_eq_meth')
    auditor_controller_task__result_more_than = NumberFilter(method='auditor_controller_more_than_meth')
    auditor_controller_task__result_less_than = NumberFilter(method='auditor_controller_less_than_meth')
    auditor_controller_task__result_contains = NumberFilter(
        field_name='auditor_controller_task__result',
        method='auditor_controller_task_result_contains_meth',
    )
    auditor_controller_task__result_not_contains = NumberFilter(
        field_name='auditor_controller_task__result',
        method='auditor_controller_task_result_not_contains_meth',
    )
    auditor_controller_task__result__discrepancy = BooleanFilter(
        method='auditor_controller_task_result_discrepancy_meth',
    )

    auditor_external_task__result_eq = NumberFilter(method='auditor_external_eq_meth')
    auditor_external_task__result_not_eq = NumberFilter(method='auditor_external_not_eq_meth')
    auditor_external_task__result_more_than = NumberFilter(method='auditor_external_more_than_meth')
    auditor_external_task__result_less_than = NumberFilter(method='auditor_external_less_than_meth')

    storage_task__result_eq = NumberFilter(method='storage_eq_meth')
    storage_task__result_not_eq = NumberFilter(method='storage_not_eq_meth')
    storage_task__result_more_than = NumberFilter(method='storage_more_than_meth')
    storage_task__result_less_than = NumberFilter(method='storage_less_than_meth')

    tsd_number_eq = NumberFilter(field_name='tsd_number', method='tsd_number_eq_meth')
    tsd_number_not_eq = NumberFilter(field_name='tsd_number', method='tsd_number_not_eq_meth')
    tsd_number_more_than = NumberFilter(field_name='tsd_number', method='tsd_number_more_than_meth')
    tsd_number_less_than = NumberFilter(field_name='tsd_number', method='tsd_number_less_than_meth')

    employee__serial_number_eq = NumberFilter(
        field_name='employee__serial_number',
        method='employee__serial_number_eq_meth',
    )
    employee__serial_number_not_eq = NumberFilter(
        field_name='employee__serial_number',
        method='employee__serial_number_not_eq_meth',
    )
    employee__serial_number_more_than = NumberFilter(
        field_name='employee__serial_number',
        method='employee__serial_number_more_than_meth',
    )
    employee__serial_number_less_than = NumberFilter(
        field_name='employee__serial_number',
        method='employee__serial_number_less_than_meth',
    )

    employee_name_eq = CharFilter(method='employee_name_eq_meth')
    employee_name_not_eq = CharFilter(method='employee_name_not_eq_meth')
    employee_name_contains = CharFilter(method='employee_name_contains_meth')
    employee_name_not_contains = CharFilter(method='employee_name_not_contains_meth')

    colors = CharInFilter(field_name='color', lookup_expr='in')

    class Meta:
        model = Document
        fields = ('project', 'fake_id')

    def project_method(self, queryset, name, value):
        return DocumentFilterSetService().project_method(queryset, name, value)

    def zone_code_start_gte(self, queryset, name, value):
        return DocumentFilterSetService().zone_code_start_gte(queryset, name, value)

    def zone_code_end_lte(self, queryset, name, value):
        return DocumentFilterSetService().zone_code_end_lte(queryset, name, value)

    def product_title_filter(self, queryset, name, value):
        return DocumentFilterSetService().product_title_filter(queryset, name, value)

    def barcode_filter(self, queryset, name, value):
        return DocumentFilterSetService().barcode_filter(queryset, name, value)

    def vendor_code_filter(self, queryset, name, value):
        return DocumentFilterSetService().vendor_code_filter(queryset, name, value)

    def start_audit_date_meth(self, queryset, name, value):
        return DocumentFilterSetService().start_audit_date_meth(queryset, name, value)

    def end_audit_date_meth(self, queryset, name, value):
        return DocumentFilterSetService().end_audit_date_meth(queryset, name, value)

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

    def fake_id_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().fake_id_eq_meth(queryset, name, value)

    def fake_id_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().fake_id_not_eq_meth(queryset, name, value)

    def fake_id_more_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().fake_id_more_than_meth(queryset, name, value)

    def fake_id_less_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().fake_id_less_than_meth(queryset, name, value)

    def zone_number_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().zone_number_eq_meth(queryset, name, value)

    def zone_number_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().zone_number_not_eq_meth(queryset, name, value)

    def zone_number_contains_meth(self, queryset, name, value):
        return DocumentFilterSetService().zone_number_contains_meth(queryset, name, value)

    def zone_number_not_contains_meth(self, queryset, name, value):
        return DocumentFilterSetService().zone_number_not_contains_meth(queryset, name, value)

    def zone_title_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().zone_title_eq_meth(queryset, name, value)

    def zone_title_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().zone_title_not_eq_meth(queryset, name, value)

    def zone_title_contains_meth(self, queryset, name, value):
        return DocumentFilterSetService().zone_title_contains_meth(queryset, name, value)

    def zone_title_not_contains_meth(self, queryset, name, value):
        return DocumentFilterSetService().zone_title_not_contains_meth(queryset, name, value)

    def counter_scan_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().counter_scan_eq_meth(queryset, name, value)

    def counter_scan_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().counter_scan_not_eq_meth(queryset, name, value)

    def counter_scan_more_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().counter_scan_more_than_meth(queryset, name, value)

    def counter_scan_less_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().counter_scan_less_than_meth(queryset, name, value)

    def controller_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().controller_eq_meth(queryset, name, value)

    def controller_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().controller_not_eq_meth(queryset, name, value)

    def controller_more_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().controller_more_than_meth(queryset, name, value)

    def controller_less_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().controller_less_than_meth(queryset, name, value)

    def auditor_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_eq_meth(queryset, name, value)

    def auditor_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_not_eq_meth(queryset, name, value)

    def auditor_more_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_more_than_meth(queryset, name, value)

    def auditor_less_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_less_than_meth(queryset, name, value)

    def auditor_task_result_contains_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_task_result_contains_meth(queryset, name, value)

    def auditor_task_result_not_contains_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_task_result_not_contains_meth(queryset, name, value)

    def auditor_controller_task_result_contains_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_controller_task_result_contains_meth(queryset, name, value)

    def auditor_task_result_discrepancy_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_task_result_discrepancy_meth(queryset, name, value)

    def auditor_controller_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_controller_eq_meth(queryset, name, value)

    def auditor_controller_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_controller_not_eq_meth(queryset, name, value)

    def auditor_controller_more_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_controller_more_than_meth(queryset, name, value)

    def auditor_controller_less_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_controller_less_than_meth(queryset, name, value)

    def auditor_controller_task_result_not_contains_meth(self, queryset, name, value):  # noqa: WPS118
        return DocumentFilterSetService().auditor_controller_task_result_not_contains_meth(queryset, name, value)

    def auditor_controller_task_result_discrepancy_meth(self, queryset, name, value):  # noqa: WPS118
        return DocumentFilterSetService().auditor_controller_task_result_discrepancy_meth(queryset, name, value)

    def auditor_external_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_external_eq_meth(queryset, name, value)

    def auditor_external_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_external_not_eq_meth(queryset, name, value)

    def auditor_external_more_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_external_more_than_meth(queryset, name, value)

    def auditor_external_less_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().auditor_external_less_than_meth(queryset, name, value)

    def storage_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().storage_eq_meth(queryset, name, value)

    def storage_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().storage_not_eq_meth(queryset, name, value)

    def storage_more_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().storage_more_than_meth(queryset, name, value)

    def storage_less_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().storage_less_than_meth(queryset, name, value)

    def tsd_number_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().tsd_number_eq_meth(queryset, name, value)

    def tsd_number_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().tsd_number_not_eq_meth(queryset, name, value)

    def tsd_number_less_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().tsd_number_less_than_meth(queryset, name, value)

    def tsd_number_more_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().tsd_number_more_than_meth(queryset, name, value)

    def employee__serial_number_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().employee__serial_number_eq_meth(queryset, name, value)

    def employee__serial_number_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().employee__serial_number_not_eq_meth(queryset, name, value)

    def employee__serial_number_more_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().employee__serial_number_more_than_meth(queryset, name, value)

    def employee__serial_number_less_than_meth(self, queryset, name, value):
        return DocumentFilterSetService().employee__serial_number_less_than_meth(queryset, name, value)

    def employee_name_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().employee_name_eq_meth(queryset, name, value)

    def employee_name_not_eq_meth(self, queryset, name, value):
        return DocumentFilterSetService().employee_name_not_eq_meth(queryset, name, value)

    def employee_name_contains_meth(self, queryset, name, value):
        return DocumentFilterSetService().employee_name_contains_meth(queryset, name, value)

    def employee_name_not_contains_meth(self, queryset, name, value):
        return DocumentFilterSetService().employee_name_not_contains_meth(queryset, name, value)


class DocumentScannedProductsFilterSet(FilterSet):
    document = NumberFilter(field_name='task__counter_scan_document', required=True)
    vendor_code = CharFilter(field_name='product__vendor_code', lookup_expr='icontains')
    barcode = CharFilter(field_name='product__barcode', lookup_expr='icontains')
    title = CharFilter(field_name='product__title', lookup_expr='icontains')

    class Meta:
        model = ScannedProduct
        fields = ('document',)
