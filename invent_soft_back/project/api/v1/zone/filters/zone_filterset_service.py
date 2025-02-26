from django.db.models import Count, Q

from api.v1.zone.serializers import ZoneReadSerializer
from apps.task.models import TaskTypeChoices
from apps.zone.models import Zone, ZoneStatusChoices
from apps.zone.services.filters.counter_scan.equal_username import ZoneFilteringByEqCounterScanUsernameService
from apps.zone.services.filters.counter_scan.not_equal_username import FilterZoneByNotEqCounterScanUsernameService


class ZoneFilterSetService():  # noqa: WPS214
    """Класс оболочка для фильтров вкладки Зоны."""

    def serial_number_gte(self, queryset, name, value):
        if value:
            return queryset.filter(serial_number__gte=value)
        return queryset

    def serial_number_lte(self, queryset, name, value):
        if value:
            return queryset.filter(serial_number__lte=value)
        return queryset

    def code_start_gte(self, queryset, name, value):
        if value:
            return queryset.filter(code__gte=value)
        return queryset

    def code_start_lte(self, queryset, name, value):
        if value:
            return queryset.filter(code__lte=value)
        return queryset

    def status_meth(self, queryset, name, value):
        if not value and value is not False:
            return queryset

        if value is True:
            return queryset.filter(status=ZoneStatusChoices.READY)
        elif value is False:
            return queryset.filter(status=ZoneStatusChoices.NOT_READY)

    def is_empty(self, queryset, name, value):
        if not value and value is not False:
            return queryset

        if value:
            return queryset.filter(tasks_scanned_products_count=0)

        return queryset.exclude(tasks_scanned_products_count=0)

    # Номер зоны

    def number_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(serial_number__exact=value)

    def number_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(serial_number__exact=value)

    def number_more_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(serial_number__gte=value)

    def number_less_than_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(serial_number__lte=value)

    # Код зоны

    def code_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(code__exact=value)

    def code_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(code__exact=value)

    def code_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(code__icontains=value)

    def code_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(code__icontains=value)

    # Название зоны

    def title_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(title__exact=value)

    def title_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(title__exact=value)

    def title_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(title__icontains=value)

    def title_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(title__icontains=value)

    # Название склада

    def storage_name_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(storage_name__exact=value)

    def storage_name_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(storage_name__exact=value)

    def storage_name_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(storage_name__icontains=value)

    def storage_name_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.exclude(storage_name__icontains=value)

    # Кол-во ШК

    def barcode_amount_eq_meth(self, queryset, name, value):
        if not value and value != 0:
            return queryset
        return queryset.filter(barcode_amount=value)

    def barcode_amount_not_eq_meth(self, queryset, name, value):
        if not value and value != 0:
            return queryset
        return queryset.exclude(barcode_amount=value)

    def barcode_amount_more_than_meth(self, queryset, name, value):
        if not value and value != 0:
            return queryset
        return queryset.filter(barcode_amount__gt=value)

    def barcode_amount_less_than_meth(self, queryset, name, value):
        if not value and value != 0:
            return queryset
        return queryset.filter(barcode_amount__lt=value)

    # С.Скан

    def cs_eq_meth(self, queryset, name, value):
        return ZoneFilteringByEqCounterScanUsernameService(queryset=queryset, counter_scan_username=value).process()

    def cs_not_eq_meth(self, queryset, name, value):
        return FilterZoneByNotEqCounterScanUsernameService(
            queryset=queryset,
            counter_scan_username=value,
        ).process()

    def cs_contains_meth(self, queryset, name, value):
        return (
            queryset
            .filter(tasks__employee__username__icontains=value, tasks__type=TaskTypeChoices.COUNTER_SCAN)
            .distinct()
        )

    def cs_not_contains_meth(self, queryset, name, value):
        return (
            queryset
            .exclude(tasks__employee__username__icontains=value, tasks__type=TaskTypeChoices.COUNTER_SCAN)
            .distinct()
        )

    def is_counter_scan_count(self, queryset, name, value):
        if value is None:
            return queryset

        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            is_counter_scan_count = serializer.data.get('is_counter_scan_count')
            if is_counter_scan_count:
                pks.append(zone.pk)

        if value:
            return queryset.filter(pk__in=pks)
        else:
            return queryset.exclude(pk__in=pks)  # noqa: WPS503

    # С.УК

    def cc_eq_meth(self, queryset, name, value):
        return (
            queryset
            .check_is_one_controller_to_zone(value=value)
            .filter(
                tasks__employee__username__iexact=value,
                tasks__type=TaskTypeChoices.CONTROLLER,
                is_one_controller_to_zone=True,
            )
            .distinct()
        )

    def cc_not_eq_meth(self, queryset, name, value):
        return (
            queryset
            .exclude(
                tasks__employee__username__iexact=value,
                tasks__type=TaskTypeChoices.CONTROLLER,
            )
            .distinct()
        )

    def cc_contains_meth(self, queryset, name, value):
        return (
            queryset
            .filter(tasks__employee__username__icontains=value, tasks__type=TaskTypeChoices.COUNTER_SCAN)
            .distinct()
        )

    def cc_not_contains_meth(self, queryset, name, value):
        return (
            queryset
            .exclude(tasks__employee__username__icontains=value, tasks__type=TaskTypeChoices.COUNTER_SCAN)
            .distinct()
        )

    def is_controller_count(self, queryset, name, value):
        if value is None:
            return queryset

        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            is_controller_count = serializer.data.get('is_controller_count')
            if is_controller_count:
                pks.append(zone.pk)

        if value:
            return queryset.filter(pk__in=pks)
        else:
            return queryset.exclude(pk__in=pks)  # noqa: WPS503

    # А.Скан

    def as_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            for employee in list(serializer.data.get('auditor')):
                username = employee.get('employee').get('username')
                if username == value and len(serializer.data.get('auditor')) == 1:
                    pks.append(zone.pk)
        return queryset.filter(pk__in=pks)

    def as_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            for employee in list(serializer.data.get('auditor')):
                if employee.get('employee').get('username') != value:
                    pks.append(zone.pk)
        return queryset.filter(pk__in=pks)

    def as_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            for employee in list(serializer.data.get('auditor')):
                if value in employee.get('employee').get('username'):
                    pks.append(zone.pk)
                    continue
        return queryset.filter(pk__in=pks)

    def as_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            in_zone = False
            for employee in list(serializer.data.get('auditor')):
                if value in employee.get('employee').get('username'):
                    in_zone = True
                    break
            if not in_zone:
                pks.append(zone.pk)
        return queryset.filter(pk__in=pks)

    def is_auditor_count(self, queryset, name, value):
        if value is None:
            return queryset

        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            is_auditor_count = serializer.data.get('is_auditor_count')
            if is_auditor_count:
                pks.append(zone.pk)

        if value:
            return queryset.filter(pk__in=pks)
        else:
            return queryset.exclude(pk__in=pks)  # noqa: WPS503

    # А.УК

    def ac_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            for employee in list(serializer.data.get('auditor_controller')):
                username = employee.get('employee').get('username')
                if username == value and len(serializer.data.get('auditor_controller')) == 1:
                    pks.append(zone.pk)
        return queryset.filter(pk__in=pks)

    def ac_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            for employee in list(serializer.data.get('auditor_controller')):
                if employee.get('employee').get('username') != value:
                    pks.append(zone.pk)
        return queryset.filter(pk__in=pks)

    def ac_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            for employee in list(serializer.data.get('auditor_controller')):
                if value in employee.get('employee').get('username'):
                    pks.append(zone.pk)
                    continue
        return queryset.filter(pk__in=pks)

    def ac_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            in_zone = False
            for employee in list(serializer.data.get('auditor_controller')):
                if value in employee.get('employee').get('username'):
                    in_zone = True
                    break
            if not in_zone:
                pks.append(zone.pk)
        return queryset.filter(pk__in=pks)

    def is_auditor_controller_count(self, queryset, name, value):
        if value is None:
            return queryset

        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            is_auditor_controller_count = serializer.data.get('is_auditor_controller_count')
            if is_auditor_controller_count:
                pks.append(zone.pk)

        if value:
            return queryset.filter(pk__in=pks)
        else:
            return queryset.exclude(pk__in=pks)  # noqa: WPS503

    # Склад

    def storage_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            for employee in list(serializer.data.get('storage')):
                username = employee.get('employee').get('username')
                if username == value and len(serializer.data.get('storage')) == 1:
                    pks.append(zone.pk)
        return queryset.filter(pk__in=pks)

    def storage_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            if len(serializer.data.get('storage')) != value:
                pks.append(zone.pk)
        return queryset.filter(pk__in=pks)

    def storage_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            for employee in list(serializer.data.get('storage')):
                if value in employee.get('employee').get('username'):
                    pks.append(zone.pk)
                    continue
        return queryset.filter(pk__in=pks)

    def storage_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset
        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            in_zone = False
            for employee in list(serializer.data.get('storage')):
                if value in employee.get('employee').get('username'):
                    in_zone = True
                    break
            if not in_zone:
                pks.append(zone.pk)
        return queryset.filter(pk__in=pks)

    def is_storage_count(self, queryset, name, value):
        if value is None:
            return queryset

        pks = []
        for zone in queryset:
            serializer = ZoneReadSerializer(zone)
            is_storage_count = serializer.data.get('is_storage_count')
            if is_storage_count:
                pks.append(zone.pk)

        if value:
            return queryset.filter(pk__in=pks)
        else:
            return queryset.exclude(pk__in=pks)  # noqa: WPS503
