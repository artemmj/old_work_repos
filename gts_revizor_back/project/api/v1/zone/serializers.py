from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.employee.models import Employee, EmployeeRoleChoices
from apps.event.models import Event, TitleChoices
from apps.helpers.serializers import EagerLoadingSerializerMixin, EnumField
from apps.project.models import Project
from apps.task.models import Task, TaskStatusChoices, TaskTypeChoices
from apps.terminal.models import Terminal
from apps.zone.models import Zone, ZoneStatusChoices


class TerminalShortReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = ('id', 'number', 'ip_address')


class EmployeeReadCompactSerializer(serializers.ModelSerializer):
    terminal = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('id', 'username', 'terminal', 'is_deleted', 'roles')

    def get_terminal(self, instance):
        return TerminalShortReadSerializer(self.context.get('terminal')).data


class ZoneTaskEmployee(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()

    select_related_fields = ('employee',)

    class Meta:
        model = Task
        fields = ('id', 'employee')

    def get_employee(self, instance):
        return EmployeeReadCompactSerializer(instance.employee, context={'terminal': self.context.get('terminal')}).data


class ZoneReadCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id', 'title', 'storage_name', 'serial_number', 'code')


class EmployeeTaskCompactReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'username', 'is_deleted')


class ZoneTaskEmployeeCompactSerializer(serializers.ModelSerializer):
    employee = EmployeeTaskCompactReadSerializer()

    class Meta:
        model = Task
        fields = ('id', 'employee')


class ZoneReadSerializer(serializers.ModelSerializer):   # noqa: WPS214
    status = EnumField(enum_class=ZoneStatusChoices)
    barcode_amount = serializers.SerializerMethodField(help_text='Кол-во ШК')
    is_empty = serializers.SerializerMethodField(help_text='Пустая')

    counter_scan = serializers.SerializerMethodField(help_text='Счетчик')
    is_counter_scan_count = serializers.SerializerMethodField(help_text='Подсчет (Счетчик)')

    controller = serializers.SerializerMethodField(help_text='УК')
    is_controller_count = serializers.SerializerMethodField(help_text='Подсчет (УК)')

    auditor = serializers.SerializerMethodField(help_text='Аудитор')
    is_auditor_count = serializers.SerializerMethodField(help_text='Подсчет (Аудитор)')

    auditor_controller = serializers.SerializerMethodField(help_text='Аудитор УК')
    is_auditor_controller_count = serializers.SerializerMethodField(help_text='Подсчет (Аудитор УК)')

    auditor_external_controller = serializers.SerializerMethodField(help_text='Внешний аудитор')
    is_auditor_external_controller_count = serializers.SerializerMethodField(help_text='Подсчет (Внешний аудитор)')

    storage = serializers.SerializerMethodField(help_text='Сотрудник склада')
    is_storage_count = serializers.SerializerMethodField(help_text='Подсчет (Склад)')

    class Meta:
        model = Zone
        fields = (
            'id',
            'serial_number',
            'title',
            'storage_name',
            'code',
            'status',
            'is_auto_assignment',
            'barcode_amount',
            'is_empty',
            'counter_scan',
            'is_counter_scan_count',
            'controller',
            'is_controller_count',
            'auditor',
            'is_auditor_count',
            'auditor_controller',
            'is_auditor_controller_count',
            'auditor_external_controller',
            'is_auditor_external_controller_count',
            'storage',
            'is_storage_count',
        )

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_barcode_amount(self, obj):
        return obj.barcode_amount

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_empty(self, obj):
        return obj.tasks_scanned_products_count == 0

    @swagger_serializer_method(serializer_or_field=ZoneTaskEmployeeCompactSerializer(many=True))
    def get_counter_scan(self, obj):
        return ZoneTaskEmployeeCompactSerializer(obj.counter_scan_tasks, many=True).data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_counter_scan_count(self, obj):
        return True if obj.counter_scan_tasks_status else False   # noqa: WPS502

    @swagger_serializer_method(serializer_or_field=ZoneTaskEmployeeCompactSerializer(many=True))
    def get_controller(self, obj):
        return ZoneTaskEmployeeCompactSerializer(obj.controller_tasks, many=True).data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_controller_count(self, obj):
        return True if obj.controller_tasks_status else False   # noqa: WPS502

    @swagger_serializer_method(serializer_or_field=ZoneTaskEmployeeCompactSerializer(many=True))
    def get_auditor(self, obj):
        return ZoneTaskEmployeeCompactSerializer(obj.auditor_tasks, many=True).data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_auditor_count(self, obj):
        return True if obj.auditor_tasks_status else False   # noqa: WPS502

    @swagger_serializer_method(serializer_or_field=ZoneTaskEmployeeCompactSerializer(many=True))
    def get_auditor_controller(self, obj):
        return ZoneTaskEmployeeCompactSerializer(obj.auditor_controller_tasks, many=True).data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_auditor_controller_count(self, obj):
        return True if obj.auditor_controller_tasks_status else False   # noqa: WPS502

    @swagger_serializer_method(serializer_or_field=ZoneTaskEmployeeCompactSerializer(many=True))
    def get_auditor_external_controller(self, obj):
        return ZoneTaskEmployeeCompactSerializer(obj.auditor_external_controller_tasks, many=True).data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_auditor_external_controller_count(self, obj):
        return True if obj.auditor_external_controller_tasks_status else False   # noqa: WPS502

    @swagger_serializer_method(serializer_or_field=ZoneTaskEmployeeCompactSerializer(many=True))
    def get_storage(self, obj):
        return ZoneTaskEmployeeCompactSerializer(obj.storage_tasks, many=True).data

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_storage_count(self, obj):
        return True if obj.storage_tasks_status else False  # noqa: WPS502


class ZoneWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id', 'serial_number', 'storage_name', 'code', 'status', 'is_auto_assignment')
        read_only_fields = ('id', 'serial_number', 'status')

    def update(self, instance, validated_data):
        if instance.is_auto_assignment is True:
            if 'is_auto_assignment' in validated_data and validated_data['is_auto_assignment'] is False:
                comment = f'Зона {instance} проекта {instance.project} исключена из автоназначения.'
                Event.objects.create(
                    project=instance.project,
                    title=TitleChoices.EXCLUDE_ZONE_FROM_AUTOASSIGNMENT,
                    comment=comment,
                )
        return super().update(instance, validated_data)


class ZoneBulkCreateSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    start_serial_number = serializers.IntegerField(min_value=1, required=True)
    amount = serializers.IntegerField(min_value=1, required=True)
    storage_name = serializers.CharField(required=False)


class ZoneBulkDeleteSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    start_serial_number = serializers.IntegerField(min_value=0, required=False)
    end_serial_number = serializers.IntegerField(min_value=1, required=False)
    zones = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all()), required=False)

    def validate(self, attrs):
        if 'zones' in attrs and 'start_serial_number' in attrs and 'end_serial_number' in attrs:
            raise ValidationError('Требуется либо параметр zones либо пара start_serial_number и end_serial_number!')
        if 'zones' not in attrs and 'start_serial_number' not in attrs and 'end_serial_number' not in attrs:
            raise ValidationError('Требуются параметры zones либо пара start_serial_number и end_serial_number!')
        if (  # noqa: WPS337
            'start_serial_number' in attrs and 'end_serial_number' not in attrs
            or 'end_serial_number' in attrs and 'start_serial_number' not in attrs
        ):
            raise ValidationError('Требуется пара параметров start_serial_number и end_serial_number!')
        return super().validate(attrs)


class ZoneIssuingTasksSerializer(serializers.Serializer):
    employees = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=True, many=True)
    role = serializers.ChoiceField(choices=EmployeeRoleChoices.choices, required=True)


class ZoneAutoAssignmentTasksSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)


class ZoneBulkUpdateSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all(), required=False)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=False)
    serial_number = serializers.IntegerField(required=False)

    title = serializers.CharField(required=False)
    storage_name = serializers.CharField(required=False)
    code = serializers.CharField(required=False)

    def validate(self, attrs):
        if 'id' not in attrs and 'project_id' not in attrs and 'serial_number' not in attrs:
            raise ValidationError('Не было передано ни одного параметра.')

        if 'id' in attrs and ('project_id' in attrs or 'serial_number' in attrs):
            raise ValidationError('Передайте либо параметр id либо параметры project_id и serial_number.')

        if (  # noqa: WPS337
            ('project_id' in attrs and 'serial_number' not in attrs)
            or ('project_id' not in attrs and 'serial_number' in attrs)
        ):
            raise ValidationError('Передайте параметр project_id вместе с serial_number.')

        return super().validate(attrs)


class BatchIssuingTasksSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    zones = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all()), required=False)
    zone_start_id = serializers.IntegerField(min_value=0, required=False)
    zone_end_id = serializers.IntegerField(min_value=1, required=False)
    employee_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all()),
        required=True,
        allow_empty=False,
    )
    role = serializers.ChoiceField(
        choices=[
            ('counter', 'Счетчик Скан'),
            ('counter_scan', 'Счетчик Скан'),
            ('controller', 'Счетчик УК'),
            ('auditor', 'Аудитор'),
            ('auditor_controller', 'Аудитор УК'),
            ('auditor_external', 'Внешний Аудитор'),
            ('storage', 'Сотрудник склада'),
        ],
        required=True,
    )

    def validate(self, attrs):
        if 'zones' in attrs and 'zone_start_id' in attrs and 'zone_end_id' in attrs:
            raise ValidationError('Требуется либо параметр zones либо пара zone_start_id и zone_end_id!')
        if 'zones' not in attrs and 'zone_start_id' not in attrs and 'zone_end_id' not in attrs:
            raise ValidationError('Требуются параметры zones либо пара zone_start_id и zone_end_id!')
        if (  # noqa: WPS337
            'zone_start_id' in attrs and 'zone_end_id' not in attrs
            or 'zone_end_id' in attrs and 'zone_start_id' not in attrs
        ):
            raise ValidationError('Требуется пара параметров zone_start_id и zone_end_id!')
        return super().validate(attrs)


class StorageNamesSerializer(serializers.Serializer):
    storage_names = serializers.ListField(child=serializers.CharField())


class InventoryInZonesReportRequestSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    document_type = serializers.ChoiceField(
        choices=[('pdf', 'PDF'), ('excel', 'Excel')],
        required=True,
    )
    group_by = serializers.ChoiceField(
        choices=[('barcode', 'По штрихкоду товара'), ('vendor_code', 'По коду товара')],
        required=True,
    )
    zones = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all()), required=False)


class ZoneBlockStatisticResponseSerializer(serializers.Serializer):
    zones_count = serializers.IntegerField()
    barcodes_sum = serializers.IntegerField()


class RolesZoneReadSerializer(ZoneReadSerializer):
    status = EnumField(enum_class=ZoneStatusChoices)
    counter_scan = serializers.SerializerMethodField()
    controller = serializers.SerializerMethodField()
    auditor = serializers.SerializerMethodField()
    auditor_controller = serializers.SerializerMethodField()
    auditor_external = serializers.SerializerMethodField()
    storage = serializers.SerializerMethodField()
    counter_rows = serializers.SerializerMethodField(help_text='Поле Кол-во записей')

    prefetch_related_fields = ('tasks', 'documents')

    class Meta:
        model = Zone
        fields = (
            'id',
            'serial_number',
            'title',
            'counter_scan',
            'controller',
            'auditor',
            'auditor_controller',
            'auditor_external',
            'storage',
            'counter_rows',
        )

    def get_counter_scan(self, instance):
        last_docs = instance.documents.all().order_by('created_at', 'status')
        if not last_docs:
            return []

        context = {'terminal': last_docs.last().terminal}
        return [ZoneTaskEmployee(last_docs.last().counter_scan_task, context=context).data]

    def get_controller(self, instance):
        last_docs = instance.documents.all().order_by('created_at', 'status')
        if not last_docs:
            return []

        context = {'terminal': last_docs.last().terminal}
        return [ZoneTaskEmployee(last_docs.last().controller_task, context=context).data]

    def get_auditor(self, instance):
        last_docs = instance.documents.all().order_by('created_at', 'status')
        if not last_docs:
            return []

        context = {'terminal': last_docs.last().terminal}
        return [ZoneTaskEmployee(last_docs.last().auditor_task, context=context).data]

    def get_auditor_controller(self, instance):
        last_docs = instance.documents.all().order_by('created_at', 'status')
        if not last_docs:
            return []

        context = {'terminal': last_docs.last().terminal}
        return [ZoneTaskEmployee(last_docs.last().auditor_controller_task, context=context).data]

    def get_auditor_external(self, instance):
        last_docs = instance.documents.all().order_by('created_at', 'status')
        if not last_docs:
            return []

        context = {'terminal': last_docs.last().terminal}
        return [ZoneTaskEmployee(last_docs.last().auditor_external_task, context=context).data]

    def get_storage(self, instance):
        last_docs = instance.documents.all().order_by('created_at', 'status')
        if not last_docs:
            return []

        context = {'terminal': last_docs.last().terminal}
        return [ZoneTaskEmployee(last_docs.last().storage_task, context=context).data]

    def get_counter_rows(self, instance) -> int:
        tasks = instance.tasks.filter(
            type=TaskTypeChoices.COUNTER_SCAN,
            status__in=(TaskStatusChoices.WORKED, TaskStatusChoices.SUCCESS_SCAN, TaskStatusChoices.FAILED_SCAN),
        )
        return sum([task.result for task in tasks])
