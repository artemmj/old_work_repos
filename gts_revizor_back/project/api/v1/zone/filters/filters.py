import logging

from django_filters import BooleanFilter, CharFilter, FilterSet, NumberFilter

from apps.zone.models import Zone

from .zone_filterset_service import ZoneFilterSetService

logger = logging.getLogger('django')


class ZoneFilterSet(FilterSet):  # noqa: WPS214
    serial_number_start = NumberFilter(field_name='serial_number', method='serial_number_gte')
    serial_number_end = NumberFilter(field_name='serial_number', method='serial_number_lte')

    code_start = CharFilter(field_name='code', method='code_start_gte')
    code_end = CharFilter(field_name='code', method='code_start_lte')

    serial_number_eq = NumberFilter(field_name='serial_number', method='number_eq_meth')
    serial_number_not_eq = NumberFilter(field_name='serial_number', method='number_not_eq_meth')
    serial_number_more_than = NumberFilter(field_name='serial_number', method='number_more_than_meth')
    serial_number_less_than = NumberFilter(field_name='serial_number', method='number_less_than_meth')

    code_eq = CharFilter(field_name='code', method='code_eq_meth')
    code_not_eq = CharFilter(field_name='code', method='code_not_eq_meth')
    code_contains = CharFilter(field_name='code', method='code_contains_meth')
    code_not_contains = CharFilter(field_name='code', method='code_not_contains_meth')

    title_eq = CharFilter(field_name='title', method='title_eq_meth')
    title_not_eq = CharFilter(field_name='title', method='title_not_eq_meth')
    title_contains = CharFilter(field_name='title', method='title_contains_meth')
    title_not_contains = CharFilter(field_name='title', method='title_not_contains_meth')

    storage_name_eq = CharFilter(field_name='storage_name', method='storage_name_eq_meth')
    storage_name_not_eq = CharFilter(field_name='storage_name', method='storage_name_not_eq_meth')
    storage_name_contains = CharFilter(field_name='storage_name', method='storage_name_contains_meth')
    storage_name_not_contains = CharFilter(field_name='storage_name', method='storage_name_not_contains_meth')

    barcode_amount_eq = NumberFilter(method='barcode_amount_eq_meth')
    barcode_amount_not_eq = NumberFilter(method='barcode_amount_not_eq_meth')
    barcode_amount_more_than = NumberFilter(method='barcode_amount_more_than_meth')
    barcode_amount_less_than = NumberFilter(method='barcode_amount_less_than_meth')

    status = BooleanFilter(field_name='status', method='status_meth')
    is_empty = BooleanFilter(method='get_is_empty')

    counter_scan_eq = CharFilter(method='cs_eq_meth')
    counter_scan_not_eq = CharFilter(method='cs_not_eq_meth')
    counter_scan_contains = CharFilter(method='cs_contains_meth')
    counter_scan_not_contains = CharFilter(method='cs_not_contains_meth')

    is_counter_scan_count = BooleanFilter(method='get_is_counter_scan_count')

    controller_eq = CharFilter(method='cc_eq_meth')
    controller_not_eq = CharFilter(method='cc_not_eq_meth')
    controller_contains = CharFilter(method='cc_contains_meth')
    controller_not_contains = CharFilter(method='cc_not_contains_meth')

    is_controller_count = BooleanFilter(method='get_is_controller_count')

    auditor_eq = CharFilter(method='as_eq_meth')
    auditor_not_eq = CharFilter(method='as_not_eq_meth')
    auditor_contains = CharFilter(method='as_contains_meth')
    auditor_not_contains = CharFilter(method='as_not_contains_meth')

    is_auditor_count = BooleanFilter(method='get_is_auditor_count')

    auditor_controller_eq = CharFilter(method='ac_eq_meth')
    auditor_controller_not_eq = CharFilter(method='ac_not_eq_meth')
    auditor_controller_contains = CharFilter(method='ac_contains_meth')
    auditor_controller_not_contains = CharFilter(method='ac_not_contains_meth')

    is_auditor_controller_count = BooleanFilter(method='get_is_auditor_controller_count')

    storage_eq = CharFilter(method='storage_eq_meth')
    storage_not_eq = CharFilter(method='storage_not_eq_meth')
    storage_contains = CharFilter(method='storage_contains_meth')
    storage_not_contains = CharFilter(method='storage_not_contains_meth')

    is_storage_count = BooleanFilter(method='get_is_storage_count')

    class Meta:
        model = Zone
        fields = ('project',)

    def serial_number_gte(self, queryset, name, value):
        return ZoneFilterSetService().serial_number_gte(queryset, name, value)

    def serial_number_lte(self, queryset, name, value):
        return ZoneFilterSetService().serial_number_lte(queryset, name, value)

    def code_start_gte(self, queryset, name, value):
        return ZoneFilterSetService().code_start_gte(queryset, name, value)

    def code_start_lte(self, queryset, name, value):
        return ZoneFilterSetService().code_start_lte(queryset, name, value)

    def status_meth(self, queryset, name, value):
        return ZoneFilterSetService().status_meth(queryset, name, value)

    def number_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().number_eq_meth(queryset, name, value)

    def number_not_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().number_not_eq_meth(queryset, name, value)

    def number_more_than_meth(self, queryset, name, value):
        return ZoneFilterSetService().number_more_than_meth(queryset, name, value)

    def number_less_than_meth(self, queryset, name, value):
        return ZoneFilterSetService().number_less_than_meth(queryset, name, value)

    def code_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().code_eq_meth(queryset, name, value)

    def code_not_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().code_not_eq_meth(queryset, name, value)

    def code_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().code_contains_meth(queryset, name, value)

    def code_not_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().code_not_contains_meth(queryset, name, value)

    def title_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().title_eq_meth(queryset, name, value)

    def title_not_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().title_not_eq_meth(queryset, name, value)

    def title_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().title_contains_meth(queryset, name, value)

    def title_not_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().title_not_contains_meth(queryset, name, value)

    def storage_name_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().storage_name_eq_meth(queryset, name, value)

    def storage_name_not_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().storage_name_not_eq_meth(queryset, name, value)

    def storage_name_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().storage_name_contains_meth(queryset, name, value)

    def storage_name_not_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().storage_name_not_contains_meth(queryset, name, value)

    def barcode_amount_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().barcode_amount_eq_meth(queryset, name, value)

    def barcode_amount_not_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().barcode_amount_not_eq_meth(queryset, name, value)

    def barcode_amount_more_than_meth(self, queryset, name, value):
        return ZoneFilterSetService().barcode_amount_more_than_meth(queryset, name, value)

    def barcode_amount_less_than_meth(self, queryset, name, value):
        return ZoneFilterSetService().barcode_amount_less_than_meth(queryset, name, value)

    def get_is_empty(self, queryset, name, value):
        return ZoneFilterSetService().is_empty(queryset, name, value)

    def cs_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().cs_eq_meth(queryset, name, value)

    def cs_not_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().cs_not_eq_meth(queryset, name, value)

    def cs_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().cs_contains_meth(queryset, name, value)

    def cs_not_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().cs_not_contains_meth(queryset, name, value)

    def get_is_counter_scan_count(self, queryset, name, value):
        return ZoneFilterSetService().is_counter_scan_count(queryset, name, value)

    def cc_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().cc_eq_meth(queryset, name, value)

    def cc_not_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().cc_not_eq_meth(queryset, name, value)

    def cc_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().cc_contains_meth(queryset, name, value)

    def cc_not_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().cc_not_contains_meth(queryset, name, value)

    def get_is_controller_count(self, queryset, name, value):
        return ZoneFilterSetService().is_controller_count(queryset, name, value)

    def as_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().as_eq_meth(queryset, name, value)

    def as_not_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().as_not_eq_meth(queryset, name, value)

    def as_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().as_contains_meth(queryset, name, value)

    def as_not_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().as_not_contains_meth(queryset, name, value)

    def get_is_auditor_count(self, queryset, name, value):
        return ZoneFilterSetService().is_auditor_count(queryset, name, value)

    def ac_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().ac_eq_meth(queryset, name, value)

    def ac_not_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().ac_not_eq_meth(queryset, name, value)

    def ac_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().ac_contains_meth(queryset, name, value)

    def ac_not_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().ac_not_contains_meth(queryset, name, value)

    def get_is_auditor_controller_count(self, queryset, name, value):
        return ZoneFilterSetService().is_auditor_controller_count(queryset, name, value)

    def storage_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().storage_eq_meth(queryset, name, value)

    def storage_not_eq_meth(self, queryset, name, value):
        return ZoneFilterSetService().storage_not_eq_meth(queryset, name, value)

    def storage_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().storage_contains_meth(queryset, name, value)

    def storage_not_contains_meth(self, queryset, name, value):
        return ZoneFilterSetService().storage_not_contains_meth(queryset, name, value)

    def get_is_storage_count(self, queryset, name, value):
        return ZoneFilterSetService().is_storage_count(queryset, name, value)
