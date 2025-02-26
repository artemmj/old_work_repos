from rest_framework import serializers

from apps.template.models import TemplatePhotos, TemplatePhotosDetail
from apps.template.services import TemplateSettingsUpdateService


class TemplatePhotosDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplatePhotosDetail
        fields = '__all__'


class TemplatePhotosSerializer(serializers.ModelSerializer):
    detail = TemplatePhotosDetailSerializer()

    class Meta:
        model = TemplatePhotos
        fields = ('id', 'is_enable', 'detail', 'order')

    def update(self, instance, validated_data):
        instance = TemplateSettingsUpdateService().process(
            instance, validated_data, self.context, serializer_class=TemplatePhotosDetailSerializer,
        )
        return instance
