from rest_framework import serializers

from apps.template.models import TemplateDocuments, TemplateDocumentsDetail
from apps.template.services import TemplateSettingsUpdateService


class TemplateDocumentsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateDocumentsDetail
        fields = '__all__'


class TemplateDocumentsSerializer(serializers.ModelSerializer):
    detail = TemplateDocumentsDetailSerializer()

    class Meta:
        model = TemplateDocuments
        fields = ('id', 'is_enable', 'detail', 'order')

    def update(self, instance, validated_data):
        instance = TemplateSettingsUpdateService().process(
            instance, validated_data, self.context, serializer_class=TemplateDocumentsDetailSerializer,
        )
        return instance
