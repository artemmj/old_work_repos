from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.file.serializers import ImageSerializer
from api.v1.template.serializers import (  # noqa: WPS235
    TemplateClientSerializer,
    TemplateCompletenessSerializer,
    TemplateDamageSerializer,
    TemplateDocumentsSerializer,
    TemplateEquipmentSerializer,
    TemplateLiftSerializer,
    TemplatePaintworkSerializer,
    TemplatePhotosSerializer,
    TemplatePlaceSerializer,
    TemplateSignaturesSerializer,
    TemplateTechnicalSerializer,
    TemplateTiresSerializer,
    TemplateVideoSerializer,
)
from api.v1.user import UserCompactSerializer
from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.template.models import (  # noqa: WPS235
    Template,
    TemplateClient,
    TemplateCompleteness,
    TemplateDamage,
    TemplateDocuments,
    TemplateDocumentsDetail,
    TemplateEquipment,
    TemplateEquipmentDetail,
    TemplateLift,
    TemplatePaintwork,
    TemplatePhotos,
    TemplatePhotosDetail,
    TemplatePlace,
    TemplateSignatures,
    TemplateTechnical,
    TemplateTires,
    TemplateTiresDetail,
    TemplateVideo,
)

User = get_user_model()

TEMPLATE_SETTINGS_MAP = {
    'equipment': [TemplateEquipment, TemplateEquipmentDetail],
    'completeness': [TemplateCompleteness],
    'documents': [TemplateDocuments, TemplateDocumentsDetail],
    'tires': [TemplateTires, TemplateTiresDetail],
    'photos': [TemplatePhotos, TemplatePhotosDetail],
    'paintwork': [TemplatePaintwork],
    'damage': [TemplateDamage],
    'technical': [TemplateTechnical],
    'lift': [TemplateLift],
    'video': [TemplateVideo],
    'place': [TemplatePlace],
    'client': [TemplateClient],
    'signatures': [TemplateSignatures],
}


class TemplateUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    equipment = TemplateEquipmentSerializer(required=False)
    completeness = TemplateCompletenessSerializer(required=False)
    documents = TemplateDocumentsSerializer(required=False)
    tires = TemplateTiresSerializer(required=False)
    photos = TemplatePhotosSerializer(required=False)
    paintwork = TemplatePaintworkSerializer(required=False)
    damage = TemplateDamageSerializer(required=False)
    technical = TemplateTechnicalSerializer(required=False)
    lift = TemplateLiftSerializer(required=False)
    video = TemplateVideoSerializer(required=False)
    place = TemplatePlaceSerializer(required=False)
    client = TemplateClientSerializer(required=False)
    signatures = TemplateSignaturesSerializer(required=False)

    class Meta:
        model = Template
        fields = (
            'id',
            'created_at',
            'title',
            'image',
            'is_active',
            'equipment',
            'completeness',
            'documents',
            'tires',
            'photos',
            'paintwork',
            'damage',
            'technical',
            'lift',
            'video',
            'place',
            'client',
            'signatures',
        )

    def update(self, instance, validated_data):  # noqa: WPS231
        if 'title' in validated_data and validated_data['title'] != instance.title:
            instance.title = validated_data.get('title')

        if 'image' in validated_data:
            instance.image = validated_data.get('image')

        if 'is_active' in validated_data:
            instance.is_active = validated_data.get('is_active')

        for field_name in TEMPLATE_SETTINGS_MAP.keys():
            field_data = validated_data.get(field_name, None)

            if field_data:
                getattr(instance, field_name).is_enable = field_data.get('is_enable')
                getattr(instance, field_name).order = field_data.get('order')
                getattr(instance, field_name).save()

                detail_data = field_data.pop('detail', '')
                if detail_data:
                    for key, value in detail_data.items():
                        setattr(getattr(instance, field_name).detail, key, value)  # noqa: WPS220
                    getattr(instance, field_name).detail.save()

        instance.save()
        return instance


class TemplateShortSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    user = UserCompactSerializer()

    class Meta:
        model = Template
        fields = ('id', 'title', 'image', 'user')


class TemplateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    equipment = TemplateEquipmentSerializer()
    completeness = TemplateCompletenessSerializer()
    documents = TemplateDocumentsSerializer()
    tires = TemplateTiresSerializer()
    photos = TemplatePhotosSerializer()
    paintwork = TemplatePaintworkSerializer()
    damage = TemplateDamageSerializer()
    technical = TemplateTechnicalSerializer()
    lift = TemplateLiftSerializer()
    video = TemplateVideoSerializer()
    place = TemplatePlaceSerializer()
    client = TemplateClientSerializer()
    signatures = TemplateSignaturesSerializer()

    class Meta:
        model = Template
        fields = (
            'id',
            'created_at',
            'title',
            'image',
            'user',
            'is_active',
            'is_main',
            'is_accreditation',
            'equipment',
            'completeness',
            'documents',
            'tires',
            'photos',
            'paintwork',
            'damage',
            'technical',
            'lift',
            'video',
            'place',
            'client',
            'signatures',
        )

    def validate(self, attrs):
        if attrs.get('is_main'):
            raise ValidationError({'error': 'Невозможно создать основной шаблон.'})
        if attrs.get('is_accreditation'):
            raise ValidationError({'error': 'Невозможно создать шаблон для аккредитации.'})
        return super().validate(attrs)

    def create(self, validated_data):
        for field, classes in TEMPLATE_SETTINGS_MAP.items():
            validated_data = self._create_settings(field, classes, validated_data)
        instance = Template.objects.create(**validated_data)
        return instance

    def _create_settings(self, field, classes, validated_data):
        data = validated_data.get(field)
        detail_data = data.pop('detail', '')
        if detail_data:
            detail = classes[1].objects.create(**detail_data)
            data['detail'] = detail
        data = classes[0].objects.create(**data)
        validated_data[field] = data
        return validated_data


class TemplateReadSerializer(EagerLoadingSerializerMixin, TemplateSerializer):
    image = ImageSerializer()
    user = UserCompactSerializer()

    select_related_fields = (
        'image',
        'equipment',
        'equipment__detail',
        'completeness',
        'documents',
        'documents__detail',
        'tires',
        'tires__detail',
        'photos',
        'photos__detail',
        'paintwork',
        'damage',
        'technical',
        'lift',
        'video',
        'place',
        'client',
        'signatures',
        'user',
    )

    class Meta(TemplateSerializer.Meta):
        pass  # noqa: WPS604


class TemplateCompactSerializer(serializers.ModelSerializer):
    user = UserCompactSerializer()
    is_usual = serializers.SerializerMethodField(help_text='Обычный шаблон')

    class Meta:
        model = Template
        fields = (
            'id',
            'title',
            'user',
            'is_usual',
            'is_main',
            'is_accreditation',
        )

    def get_is_usual(self, obj) -> bool:
        return not obj.is_main and not obj.is_accreditation


class ForCreateTemplateServiceSerializer(TemplateSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, attrs):
        return attrs
