from django.db.models import Sum
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.task.serializers import TaskReadSerializer
from apps.employee.models import Employee, EmployeeRoleChoices
from apps.helpers.serializers import EagerLoadingSerializerMixin, EnumField
from apps.project.models import IssuingTaskChoices, Project
from apps.task.models import TaskStatusChoices, TaskTypeChoices


class EmployeeShortReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'serial_number', 'username', 'is_deleted', 'is_auto_assignment', 'roles')


class EmployeeRetrieveSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    roles = serializers.ListField(child=EnumField(enum_class=EmployeeRoleChoices))
    tasks = serializers.SerializerMethodField(help_text='Зоны')

    prefetch_related_fields = ('tasks',)

    class Meta:
        model = Employee
        fields = (
            'id',
            'serial_number',
            'username',
            'roles',
            'is_deleted',
            'is_auto_assignment',
            'terminal',
            'tasks',
        )

    @swagger_serializer_method(serializer_or_field=TaskReadSerializer)
    def get_tasks(self, employee):
        return TaskReadSerializer(employee.initialized_tasks, many=True).data


class EmployeeReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    roles = serializers.ListField(child=EnumField(enum_class=EmployeeRoleChoices))
    norm = serializers.SerializerMethodField(help_text='Норма')
    counter_scan = serializers.SerializerMethodField(help_text='Счетчик')
    controller = serializers.SerializerMethodField(help_text='УК')
    auditor = serializers.SerializerMethodField(help_text='Аудитор')
    auditor_controller = serializers.SerializerMethodField(help_text='Аудитор УК')
    auditor_external = serializers.SerializerMethodField(help_text='Внешник аудитор')
    storage = serializers.SerializerMethodField(help_text='Сотрудник склада')

    select_related_fields = ('project',)
    prefetch_related_fields = ('tasks',)

    class Meta:
        model = Employee
        fields = (
            'id',
            'serial_number',
            'username',
            'roles',
            'is_deleted',
            'is_auto_assignment',
            'norm',
            'counter_scan',
            'controller',
            'auditor',
            'auditor_controller',
            'auditor_external',
            'storage',
        )

    def get_norm(self, obj) -> int:
        return obj.project.rmm_settings.norm

    def get_counter_scan(self, obj) -> int:
        return obj.tasks.filter(type=TaskTypeChoices.COUNTER_SCAN).aggregate(sum=Sum('result'))['sum'] or 0

    def get_controller(self, obj) -> int:
        return obj.tasks.filter(type=TaskTypeChoices.CONTROLLER).aggregate(sum=Sum('result'))['sum'] or 0

    def get_auditor(self, obj) -> int:
        return obj.tasks.filter(type=TaskTypeChoices.AUDITOR).aggregate(sum=Sum('result'))['sum'] or 0

    def get_auditor_controller(self, obj) -> int:
        return obj.tasks.filter(type=TaskTypeChoices.AUDITOR_CONTROLLER).aggregate(sum=Sum('result'))['sum'] or 0

    def get_auditor_external(self, obj) -> int:
        return obj.tasks.filter(type=TaskTypeChoices.AUDITOR_EXTERNAL).aggregate(sum=Sum('result'))['sum'] or 0

    def get_storage(self, obj) -> int:
        return obj.tasks.filter(type=TaskTypeChoices.STORAGE).aggregate(sum=Sum('result'))['sum'] or 0


class EmployeeWideSerializer(EmployeeRetrieveSerializer, EmployeeReadSerializer):
    pass  # noqa: WPS420 WPS604


class EmployeeBulkCreateSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    start_serial_number = serializers.IntegerField(min_value=0, required=True)
    amount = serializers.IntegerField(min_value=1, required=True)
    roles = serializers.ListField(
        child=serializers.ChoiceField(
            choices=(  # noqa: WPS317
                'counter', 'Счетчик',
                'controller', 'УК',
                'auditor', 'Аудитор',
                'auditor_external', 'ВНешний аудитор',
                'storage', 'Сотрудник склада',
            ),
        ),
        required=True,
    )

    def validate(self, attrs):
        project = attrs['project']
        amount = attrs['amount']
        issuing_task = project.terminal_settings.issuing_task
        least_loaded_user = IssuingTaskChoices.LEAST_LOADED_USER
        if issuing_task == least_loaded_user and project.employees.all().count() == 0 and amount <= 1:
            raise ValidationError(
                {'error': 'Колличество необходимо указать больше 1'},
            )
        return super().validate(attrs)


class EmployeeBulkDeleteSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
    start_serial_number = serializers.IntegerField(min_value=0, required=True)
    end_serial_number = serializers.IntegerField(min_value=1, required=True)


class EmployeeExportRequestSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=True)
