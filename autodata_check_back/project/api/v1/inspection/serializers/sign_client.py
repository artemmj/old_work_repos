from constance import config
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.file.serializers import ImageSerializer
from api.v1.inspection.serializers.services import ValidateInspectionsAttrService
from apps.file.models import Image
from apps.inspection.models.inspection import Inspection
from apps.inspection.models.sign_client import SignClient


class SignClientCreateSerializer(serializers.ModelSerializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    inspection = serializers.PrimaryKeyRelatedField(queryset=Inspection.objects.all(), required=False)

    class Meta:
        model = SignClient
        fields = ('id', 'created_at', 'image', 'inspection', 'accreditation_inspection')

    def validate(self, attrs):
        if self.context['request'].method not in {'PATCH', 'PUT'}:
            ValidateInspectionsAttrService(attrs=attrs).process()

        return super().validate(attrs)

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
        except IntegrityError:
            raise ValidationError({'inspection': config.INSPECTION_IMPOSSIBLE_BIND_CLIENT_SIGN_ERROR})
        return instance


class SignClientRetrieveSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = SignClient
        fields = ('id', 'created_at', 'image')
