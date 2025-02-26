from rest_framework import serializers

from apps.template.models import TemplateTires, TemplateTiresDetail
from apps.template.services import TemplateSettingsUpdateService


class TemplateTiresDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateTiresDetail
        fields = '__all__'


class TemplateTiresSerializer(serializers.ModelSerializer):
    detail = TemplateTiresDetailSerializer()

    class Meta:
        model = TemplateTires
        fields = ('id', 'is_enable', 'detail', 'order')

    def update(self, instance, validated_data):
        instance = TemplateSettingsUpdateService().process(
            instance, validated_data, self.context, serializer_class=TemplateTiresDetailSerializer,
        )
        return instance
