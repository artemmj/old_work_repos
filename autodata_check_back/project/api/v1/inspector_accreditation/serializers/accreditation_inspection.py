from rest_framework import serializers

from api.v1.address.serializers import AddressReadSerializer
from api.v1.car.serializers.car import CarReadSerializer
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
from api.v1.template.serializers import TemplateReadSerializer
from apps.helpers.serializers import EnumField
from apps.inspector_accreditation.models import AccreditationInspection, StatusChoices


class AccreditationInspectionReadSerializer(serializers.ModelSerializer):
    status = EnumField(enum_class=StatusChoices)
    template = TemplateReadSerializer()
    address = AddressReadSerializer()
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

    class Meta:
        model = AccreditationInspection
        fields = (
            'id',
            'created_at',
            'address',
            'status',
            'template',
            'comment',
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
            'sign_client',
            'sign_inspector',
        )


class AccreditationInspectionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccreditationInspection
        fields = ('id', 'created_at', 'address', 'status', 'template', 'comment')
        read_only_fields = ('id', 'created_at', 'template')

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if 'comment' in validated_data:
            instance.status = StatusChoices.TROUBLESHOOTING
            instance.save()
        return instance
