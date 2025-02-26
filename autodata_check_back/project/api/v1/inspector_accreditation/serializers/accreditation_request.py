from constance import config
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.city.serializers import CityReadSerializer
from api.v1.file.serializers import ImageSerializer
from api.v1.inspector.serializers import InspectorSerializer
from api.v1.inspector_accreditation.serializers import AccreditationInspectionReadSerializer
from apps.address.models.city import City
from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.inspector_accreditation.models import InspectorAccreditationRequest
from apps.user.models import User


class UserInspectorSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    avatar = ImageSerializer(required=False)
    inspector = serializers.SerializerMethodField()

    select_related_fields = ('avatar',)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'avatar', 'inspector')

    @swagger_serializer_method(InspectorSerializer)
    def get_inspector(self, instance):
        if instance.inspectors.all():
            return InspectorSerializer(instance.inspectors.first()).data
        return None


class InspectorAccreditationRequestReadSerializer(serializers.ModelSerializer):
    user = UserInspectorSerializer()
    accreditation_inspection = AccreditationInspectionReadSerializer()
    city = CityReadSerializer()

    class Meta:
        model = InspectorAccreditationRequest
        fields = (
            'id',
            'created_at',
            'user',
            'inn',
            'work_skills',
            'company',
            'city',
            'radius',
            'availability_thickness_gauge',
            'accreditation_inspection',
        )
        read_only_fields = ('id', 'created_at', 'user', 'accreditation_inspection')


class InspectorAccreditationRequestCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), read_only=False)

    class Meta:
        model = InspectorAccreditationRequest
        fields = (
            'id',
            'created_at',
            'user',
            'inn',
            'work_skills',
            'company',
            'city',
            'radius',
            'availability_thickness_gauge',
        )
        read_only_fields = ('id', 'created_at', 'user')

    def create(self, validated_data):
        if InspectorAccreditationRequest.objects.filter(user=validated_data['user']).exists():
            raise ValidationError({'user': config.ACCRED_USER_HAVE_REQUEST_ERROR})
        return super().create(validated_data)
