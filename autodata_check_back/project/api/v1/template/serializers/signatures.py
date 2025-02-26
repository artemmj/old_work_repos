from rest_framework import serializers

from apps.template.models import TemplateSignatures
from apps.template.services import TemplateSettingsUpdateService


class TemplateSignaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateSignatures
        fields = ('id', 'is_enable', 'order')

    def update(self, instance, validated_data):
        instance = TemplateSettingsUpdateService().process(
            instance, validated_data, self.context,
        )
        return instance
