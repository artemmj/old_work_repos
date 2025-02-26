from rest_framework import serializers

from apps.template.models import TemplatePlace
from apps.template.services import TemplateSettingsUpdateService


class TemplatePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplatePlace
        fields = ('id', 'is_enable', 'order')

    def update(self, instance, validated_data):
        instance = TemplateSettingsUpdateService().process(
            instance, validated_data, self.context,
        )
        return instance
