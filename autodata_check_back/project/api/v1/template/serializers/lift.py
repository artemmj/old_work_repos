from rest_framework import serializers

from apps.template.models import TemplateLift
from apps.template.services import TemplateSettingsUpdateService


class TemplateLiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateLift
        fields = ('id', 'is_enable', 'order')

    def update(self, instance, validated_data):
        instance = TemplateSettingsUpdateService().process(
            instance, validated_data, self.context,
        )
        return instance
