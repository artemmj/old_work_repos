from rest_framework import serializers

from apps.template.models import TemplatePaintwork
from apps.template.services import TemplateSettingsUpdateService


class TemplatePaintworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplatePaintwork
        fields = ('id', 'is_enable', 'order')

    def update(self, instance, validated_data):
        instance = TemplateSettingsUpdateService().process(
            instance, validated_data, self.context,
        )
        return instance
