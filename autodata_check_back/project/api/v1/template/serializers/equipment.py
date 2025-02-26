from rest_framework import serializers

from apps.template.models import TemplateEquipment, TemplateEquipmentDetail
from apps.template.services import TemplateSettingsUpdateService


class TemplateEquipmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateEquipmentDetail
        fields = '__all__'


class TemplateEquipmentSerializer(serializers.ModelSerializer):
    detail = TemplateEquipmentDetailSerializer()

    class Meta:
        model = TemplateEquipment
        fields = ('id', 'is_enable', 'detail', 'order')

    def update(self, instance, validated_data):
        instance = TemplateSettingsUpdateService().process(
            instance, validated_data, self.context, serializer_class=TemplateEquipmentDetailSerializer,
        )
        return instance
