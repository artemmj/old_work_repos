from apps.task.models import TaskTypeChoices
from apps.zone.models import ZoneStatusChoices


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

    # Счетчик

    def cs_eq_meth(self, queryset, name, value):
        if not value:
            return queryset

        task_type = TaskTypeChoices.COUNTER_SCAN

        return (
            queryset
            .check_is_one_employee_to_zone(value, task_type)
            .filter(
                tasks__employee__username__exact=value,
                tasks__type=task_type,
                is_one_employee_to_zone=True,
            )
            .distinct()
        )

    def cs_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset

        task_type = TaskTypeChoices.COUNTER_SCAN

        return (
            queryset
            .check_is_one_employee_to_zone(value, task_type)
            .exclude(
                tasks__employee__username__exact=value,
                tasks__type=task_type,
                is_one_employee_to_zone=True,
            )
            .distinct()
        )

    def cs_contains_meth(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .filter(
                tasks__employee__username__icontains=value,
                tasks__type=TaskTypeChoices.COUNTER_SCAN,
            )
            .distinct()
        )

    def cs_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .exclude(tasks__employee__username__icontains=value, tasks__type=TaskTypeChoices.COUNTER_SCAN)
            .distinct()
        )

    def is_counter_scan_count(self, queryset, name, value):
        if not value and value is not False:
            return queryset

        task_type = TaskTypeChoices.COUNTER_SCAN
        queryset = queryset.check_is_one_employee_to_zone(value, task_type)

        return queryset.filter(is_tasks=True) if value else queryset.filter(is_tasks=False)

    # УК

    def cc_eq_meth(self, queryset, name, value):
        if not value:
            return queryset

        task_type = TaskTypeChoices.CONTROLLER

        return (
            queryset
            .check_is_one_employee_to_zone(value, task_type)
            .filter(
                tasks__employee__username__exact=value,
                tasks__type=task_type,
                is_one_employee_to_zone=True,
            )
            .distinct()
        )

    def cc_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset

        task_type = TaskTypeChoices.CONTROLLER

        return (
            queryset
            .check_is_one_employee_to_zone(value, task_type)
            .exclude(
                tasks__employee__username__exact=value,
                tasks__type=TaskTypeChoices.CONTROLLER,
                is_one_employee_to_zone=True,
            )
            .distinct()
        )

    def cc_contains_meth(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .filter(
                tasks__employee__username__icontains=value,
                tasks__type=TaskTypeChoices.CONTROLLER,
            )
            .distinct()
        )

    def cc_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .exclude(tasks__employee__username__icontains=value, tasks__type=TaskTypeChoices.CONTROLLER)
            .distinct()
        )

    def is_controller_count(self, queryset, name, value):
        if not value and value is not False:
            return queryset

        task_type = TaskTypeChoices.CONTROLLER
        queryset = queryset.check_is_one_employee_to_zone(value, task_type)

        return queryset.filter(is_tasks=True) if value else queryset.filter(is_tasks=False)

    # Аудитор

    def as_eq_meth(self, queryset, name, value):
        if not value:
            return queryset

        task_type = TaskTypeChoices.AUDITOR

        return (
            queryset
            .check_is_one_employee_to_zone(value, task_type)
            .filter(
                tasks__employee__username__exact=value,
                tasks__type=task_type,
                is_one_employee_to_zone=True,
            )
            .distinct()
        )

    def as_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset

        task_type = TaskTypeChoices.AUDITOR

        return (
            queryset
            .check_is_one_employee_to_zone(value, task_type)
            .exclude(
                tasks__employee__username__exact=value,
                tasks__type=task_type,
                is_one_employee_to_zone=True,
            )
            .distinct()
        )

    def as_contains_meth(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .filter(
                tasks__employee__username__icontains=value,
                tasks__type=TaskTypeChoices.AUDITOR,
            )
            .distinct()
        )

    def as_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .exclude(tasks__employee__username__icontains=value, tasks__type=TaskTypeChoices.AUDITOR)
            .distinct()
        )

    def is_auditor_count(self, queryset, name, value):
        if not value and value is not False:
            return queryset

        task_type = TaskTypeChoices.AUDITOR
        queryset = queryset.check_is_one_employee_to_zone(value, task_type)

        return queryset.filter(is_tasks=True) if value else queryset.filter(is_tasks=False)

    # Аудитор УК

    def ac_eq_meth(self, queryset, name, value):
        if not value:
            return queryset

        task_type = TaskTypeChoices.AUDITOR_CONTROLLER

        return (
            queryset
            .check_is_one_employee_to_zone(value, task_type)
            .filter(
                tasks__employee__username__exact=value,
                tasks__type=task_type,
                is_one_employee_to_zone=True,
            )
            .distinct()
        )

    def ac_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset

        task_type = TaskTypeChoices.AUDITOR_CONTROLLER

        return (
            queryset
            .check_is_one_employee_to_zone(value, task_type)
            .exclude(
                tasks__employee__username__exact=value,
                tasks__type=task_type,
                is_one_employee_to_zone=True,
            )
            .distinct()
        )

    def ac_contains_meth(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .filter(
                tasks__employee__username__icontains=value,
                tasks__type=TaskTypeChoices.AUDITOR_CONTROLLER,
            )
            .distinct()
        )

    def ac_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .exclude(tasks__employee__username__icontains=value, tasks__type=TaskTypeChoices.AUDITOR_CONTROLLER)
            .distinct()
        )

    def is_auditor_controller_count(self, queryset, name, value):
        if not value and value is not False:
            return queryset

        task_type = TaskTypeChoices.AUDITOR_CONTROLLER
        queryset = queryset.check_is_one_employee_to_zone(value, task_type)

        return queryset.filter(is_tasks=True) if value else queryset.filter(is_tasks=False)

    # Склад

    def storage_eq_meth(self, queryset, name, value):
        if not value:
            return queryset

        task_type = TaskTypeChoices.STORAGE

        return (
            queryset
            .check_is_one_employee_to_zone(value, task_type)
            .filter(
                tasks__employee__username__exact=value,
                tasks__type=task_type,
                is_one_employee_to_zone=True,
            )
            .distinct()
        )

    def storage_not_eq_meth(self, queryset, name, value):
        if not value:
            return queryset

        task_type = TaskTypeChoices.STORAGE

        return (
            queryset
            .check_is_one_employee_to_zone(value, task_type)
            .exclude(
                tasks__employee__username__exact=value,
                tasks__type=task_type,
                is_one_employee_to_zone=True,
            )
            .distinct()
        )

    def storage_contains_meth(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .filter(
                tasks__employee__username__icontains=value,
                tasks__type=TaskTypeChoices.STORAGE,
            )
            .distinct()
        )

    def storage_not_contains_meth(self, queryset, name, value):
        if not value:
            return queryset

        return (
            queryset
            .exclude(tasks__employee__username__icontains=value, tasks__type=TaskTypeChoices.STORAGE)
            .distinct()
        )

    def is_storage_count(self, queryset, name, value):
        if not value and value is not False:
            return queryset

        task_type = TaskTypeChoices.STORAGE
        queryset = queryset.check_is_one_employee_to_zone(value, task_type)

        return queryset.filter(is_tasks=True) if value else queryset.filter(is_tasks=False)
