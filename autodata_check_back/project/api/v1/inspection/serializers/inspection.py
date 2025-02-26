from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from api.v1.address.serializers import AddressReadSerializer
from api.v1.car.serializers.car import CarCompactSerializer, CarReadSerializer
from api.v1.inspection.serializers.client import ClientReadSerializer
from api.v1.inspection.serializers.completeness import CompletenessReadSerializer
from api.v1.inspection.serializers.damage import DamageReadSerializer
from api.v1.inspection.serializers.documents import DocumentsReadSerializer
from api.v1.inspection.serializers.equipment import EquipmentReadSerializer
from api.v1.inspection.serializers.lift import LiftReadSerializer
from api.v1.inspection.serializers.paintwork import PaintworkReadSerializer
from api.v1.inspection.serializers.photos import PhotosReadSerializer
from api.v1.inspection.serializers.sign_client import SignClientRetrieveSerializer
from api.v1.inspection.serializers.sign_inspector import SignInspectorRetrieveSerializer
from api.v1.inspection.serializers.technical import TechnicalReadSerializer
from api.v1.inspection.serializers.tires import TiresReadSerializer
from api.v1.inspection.serializers.video import VideoReadSerializer
from api.v1.inspection_task.serializers import InspectionTaskReadSerializer
from api.v1.organization.serializers.organization import OrganizationReadCompactSerializer
from api.v1.user import UserCompactSerializer
from apps.address.models.address import Address
from apps.helpers.serializers import EagerLoadingSerializerMixin, EnumField, EnumSerializer
from apps.inspection.models.inspection import Inspection, StatusChoices
from apps.inspection.models.inspection_note import InspectionNote
from apps.template.models import Template

User = get_user_model()


class InspectionReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):  # noqa: WPS214
    car = CarReadSerializer()
    equipment = EquipmentReadSerializer()
    completeness = CompletenessReadSerializer()
    documents = DocumentsReadSerializer()
    tires = TiresReadSerializer()
    photos = PhotosReadSerializer()
    video = VideoReadSerializer()
    paintwork = PaintworkReadSerializer()
    damage = DamageReadSerializer()
    technical = TechnicalReadSerializer()
    lift = LiftReadSerializer()
    client = ClientReadSerializer()
    sign_client = SignClientRetrieveSerializer()
    sign_inspector = SignInspectorRetrieveSerializer()
    status = EnumField(enum_class=StatusChoices)
    inspector = UserCompactSerializer()
    address = AddressReadSerializer()
    task = InspectionTaskReadSerializer()
    organization = OrganizationReadCompactSerializer()

    select_related_fields = (
        'car',
        'equipment',
        'completeness',
        'documents',
        'tires',
        'photos',
        'video',
        'paintwork',
        'damage',
        'technical',
        'lift',
        'client',
        'inspector',
        'inspector__avatar',
        'sign_client',
        'sign_inspector',
        'address',
        'task',
    )

    class Meta:
        model = Inspection
        fields = (
            'id',
            'car',
            'equipment',
            'completeness',
            'inspector',
            'documents',
            'tires',
            'photos',
            'video',
            'paintwork',
            'damage',
            'technical',
            'lift',
            'client',
            'sign_client',
            'sign_inspector',
            'status',
            'template',
            'organization',
            'address',
            'task',
            'updated_at',
            'complete_date',
            'type',
        )


class InspectionCompactSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    car = CarCompactSerializer()
    photos = PhotosReadSerializer()
    status = EnumField(enum_class=StatusChoices)
    inspector = serializers.SerializerMethodField()

    select_related_fields = ('car__brand', 'car__model', 'photos', 'inspector')

    class Meta:
        model = Inspection
        fields = ('id', 'created_at', 'car', 'photos', 'inspector', 'status', 'updated_at', 'complete_date')

    def get_inspector(self, obj) -> str:
        return f'{obj.inspector.last_name} {obj.inspector.first_name}'  # noqa: WPS237


class InspectionWriteSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    inspector = serializers.HiddenField(default=CurrentUserDefault())
    template = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all(), required=True)
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required=False)

    class Meta:
        model = Inspection
        fields = (
            'id',
            'inspector',
            'organization',
            'task',
            'status',
            'address',
            'comment',
            'template',
            'is_public',
        )
        read_only_fields = ('id',)


class InspectionAdminCompactQuerySerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)


class InspectionAdminCompactSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    car = CarCompactSerializer()
    organization = OrganizationReadCompactSerializer()
    inspector = UserCompactSerializer()

    select_related_fields = ('car',)

    class Meta:
        model = Inspection
        fields = ('id', 'status', 'car', 'organization', 'inspector', 'complete_date', 'is_public', 'template')

    def get_status(self, instance):
        return {
            'name': instance.get_status_display(),
            'value': instance.status,
        }


class LeaveNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionNote
        fields = ('id', 'created_at', 'text', 'inspection')
        read_only_fields = ('id', 'created_at')


class InspectionsListSerializer(serializers.ModelSerializer):
    brand_model = serializers.SerializerMethodField()
    vin_code = serializers.SerializerMethodField()
    fio = serializers.SerializerMethodField()
    organization_title = serializers.SerializerMethodField()
    task_id = serializers.CharField(source='task.id', allow_null=True)
    task_created_at = serializers.CharField(source='task.created_at', allow_null=True)
    task_status = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    organization_id = serializers.CharField(source='organization.pk')
    inspection_id = serializers.CharField(source='pk')

    class Meta:
        model = Inspection
        fields = (
            'id',
            'brand_model',
            'vin_code',
            'fio',
            'organization_title',
            'task_id',
            'task_created_at',
            'task_status',
            'price',
            'is_public',
            'organization_id',
            'inspection_id',
        )

    def get_brand_model(self, instance: Inspection):
        if getattr(instance, 'car', None):
            brand_title = instance.car.brand.title
            model_title = instance.car.model.title
            return f'{brand_title} {model_title}'
        return None

    def get_vin_code(self, instance: Inspection):
        if getattr(instance, 'car', None):
            return instance.car.vin_code

    def get_fio(self, instance: Inspection):
        if getattr(instance, 'inspector', None):
            fname = instance.inspector.first_name
            lname = instance.inspector.last_name
            return f'{fname} {lname}'

    def get_organization_title(self, instance: Inspection):
        if getattr(instance, 'organization', None):
            return instance.organization.title

    def get_task_status(self, instance: Inspection):
        if getattr(instance, 'task', None):
            return instance.task.get_status_display()

    def get_price(self, instance: Inspection):
        if getattr(instance, 'task', None) and instance.task.organization.self_inspection_price:
            return '%.2f' % instance.task.organization.self_inspection_price  # noqa: WPS323
