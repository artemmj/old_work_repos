from datetime import datetime, timedelta
from logging import getLogger

from constance import config
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.address.serializers import AddressReadSerializer
from api.v1.car.serializers.brand import BrandSerializer
from api.v1.car.serializers.category import CategorySerializer
from api.v1.car.serializers.model import ModelCompactSerializer
from api.v1.organization.serializers.organization import OrganizationReadCompactSerializer
from api.v1.user.serializers import UserCompactSerializer
from apps.helpers.serializers import EagerLoadingSerializerMixin, EnumField
from apps.inspection.models.inspection import Inspection, StatusChoices
from apps.inspection_task.models.task import InspectionTask, InspectionTaskCar, InspectorTaskStatuses

User = get_user_model()
logger = getLogger('django')


class InspectionTaskCarSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    inspection_status = serializers.SerializerMethodField()
    inspection_updated_at = serializers.SerializerMethodField()
    note_btn_enabled = serializers.SerializerMethodField()
    accept_btn_enabled = serializers.SerializerMethodField()

    select_related_fields = ('inspection',)

    class Meta:
        model = InspectionTaskCar
        fields = (
            'id',
            'serial_number',
            'category',
            'brand',
            'model',
            'vin_code',
            'unstandart_vin',
            'inspection',
            'inspection_status',
            'inspection_updated_at',
            'note_btn_enabled',
            'accept_btn_enabled',
        )

    def validate(self, attrs):
        serial_number = attrs.get('serial_number')
        task = self.context['task']
        if InspectionTaskCar.objects.filter(serial_number=serial_number, task=task).exists():
            raise ValidationError(
                config.TASK_CAR_VALIDATE_SERIAL_NUM_ERROR.replace('serial_number', str(serial_number)),
            )
        return attrs

    def create(self, validated_data):
        validated_data['task'] = self.context['task']
        return super().create(validated_data)

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_inspection_status(self, instance):
        return instance.inspection.status if instance.inspection else None

    @swagger_serializer_method(serializer_or_field=serializers.DateTimeField)
    def get_inspection_updated_at(self, instance):
        return instance.inspection.updated_at if instance.inspection else None

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_note_btn_enabled(self, instance):
        if not instance.inspection:
            return False

        return instance.inspection.status in {
            StatusChoices.COMPLETE,
            StatusChoices.UNDER_REVIEW,
            StatusChoices.ACCEPTED,
        }

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_accept_btn_enabled(self, instance):
        if not instance.inspection:
            return False

        return instance.inspection.status in {
            StatusChoices.COMPLETE,
            StatusChoices.UNDER_REVIEW,
        }


class InspectionTaskCarReadSerializer(InspectionTaskCarSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    model = ModelCompactSerializer()


class InspectionTaskReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    cars = InspectionTaskCarReadSerializer(source='inspection_task_cars', many=True)
    author = UserCompactSerializer()
    inspector = UserCompactSerializer()
    address = AddressReadSerializer()
    status = EnumField(enum_class=InspectorTaskStatuses)
    activity_time = serializers.SerializerMethodField(help_text='Время на активность инспектора')
    organization = OrganizationReadCompactSerializer()
    invitations_count = serializers.SerializerMethodField()

    select_related_fields = ('inspector', 'inspector__avatar', 'address')
    prefetch_related_fields = (
        'inspection_task_cars',
        'inspection_task_cars__category',
        'inspection_task_cars__brand',
        'inspection_task_cars__model',
    )

    class Meta:
        model = InspectionTask
        fields = (
            'id',
            'author',
            'inspector',
            'organization',
            'created_at',
            'cars',
            'fio',
            'phone',
            'address',
            'start_date',
            'end_date',
            'planed_date',
            'planed_date_confirm',
            'activity_time',
            'status',
            'last_status_change_date',
            'inspector_amount',
            'organization_amount',
            'type',
            'invitations_count',
        )
        read_only_fields = ('id', 'created_at')

    @swagger_serializer_method(serializer_or_field=serializers.DateTimeField)
    def get_activity_time(self, obj):
        if obj.accepted_datetime and obj.status == InspectorTaskStatuses.TASK_ACCEPTED:
            return obj.accepted_datetime + timedelta(hours=config.INSPECTION_TASK_ACTIVITY_TIME)
        return None

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_invitations_count(self, instance):
        return instance.invitations.count()


class InspectionTaskWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = InspectionTask
        fields = (
            'id',
            'author',
            'inspector',
            'organization',
            'created_at',
            'fio',
            'phone',
            'address',
            'start_date',
            'end_date',
            'planed_date',
            'planed_date_confirm',
            'status',
        )
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        planed_date = attrs.get('planed_date')
        if self.instance and planed_date and self.instance.end_date < planed_date:
            raise ValidationError(
                {'error': config.TASK_VALIDATE_DATE_ERROR.replace('DATE', str(self.instance.end_date))},
            )
        return attrs


class InspectionTaskAdminCompactQuerySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)


class InspectionTaskAdminCompactSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    cars = InspectionTaskCarReadSerializer(source='inspection_task_cars', many=True)
    cars_count = serializers.IntegerField(help_text='Кол-во автомобилей')
    status = EnumField(enum_class=InspectorTaskStatuses)

    prefetch_related_fields = (
        'inspection_task_cars',
        'inspection_task_cars__category',
        'inspection_task_cars__brand',
        'inspection_task_cars__model',
    )

    class Meta:
        model = InspectionTask
        fields = ('id', 'created_at', 'end_date', 'cars', 'cars_count', 'status', 'organization_amount')


class InspectionTaskAppointmentSerializer(serializers.Serializer):
    inspector = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
