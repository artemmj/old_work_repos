from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.event.models import Event, TitleChoices
from apps.file.models import File
from apps.helpers.serializers import EnumField, TemplateFieldEnum
from apps.project.models import Project
from apps.template.models import (
    Template,
    TemplateExport,
    TemplateExportFieldChoices,
    TemplateField,
    TemplateFieldChoices,
)


class TemplateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'title', 'field_separator', 'decimal_separator', 'fields')

    def validate(self, attrs):
        if len(attrs.get('fields')) > 30:
            raise ValidationError('Невозможно выбрать более 30 пунктов')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        project = Project.objects.filter(template=instance)
        Event.objects.create(
            project=project[0] if project else None,
            title=TitleChoices.CHANGE_TEMPLATE,
            comment=f'Обновлен шаблон загрузки {instance.title}',
        )
        return super().update(instance, validated_data)


class TemplateReadSerializer(serializers.ModelSerializer):
    fields = serializers.ListField(child=EnumField(enum_class=TemplateFieldChoices))

    class Meta:
        model = Template
        fields = ('id', 'title', 'field_separator', 'decimal_separator', 'fields')


class TemplateRetrieveResponseSerializer(serializers.ModelSerializer):
    fields = serializers.ListField(child=TemplateFieldEnum(enum_class=TemplateFieldChoices))

    class Meta:
        model = Template
        fields = ('id', 'title', 'field_separator', 'decimal_separator', 'fields')


class TemplateExportWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateExport
        fields = (
            'id',
            'title',
            'field_separator',
            'decimal_separator',
            'storage_name',
            'single_export',
            'fields',
            'zone_number_start',
            'zone_number_end',
            'is_products_find_by_code',
            'is_products_find_by_qr_code',
        )

    def validate(self, attrs):
        if len(attrs.get('fields')) > 40:
            raise ValidationError('Невозможно выбрать более 40 пунктов')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        project = Project.objects.filter(template_export=instance)
        Event.objects.create(
            project=project[0] if project else None,
            title=TitleChoices.CHANGE_TEMPLATE,
            comment=f'Обновлен шаблон выгрузки {instance.title}',
        )
        return super().update(instance, validated_data)


class TemplateExportReadSerializer(serializers.ModelSerializer):
    fields = serializers.ListField(child=EnumField(enum_class=TemplateExportFieldChoices))

    class Meta:
        model = TemplateExport
        fields = (
            'id',
            'title',
            'field_separator',
            'decimal_separator',
            'storage_name',
            'single_export',
            'fields',
            'zone_number_start',
            'zone_number_end',
            'is_products_find_by_code',
            'is_products_find_by_qr_code',
        )


class TemplateExportFieldsResponseSerializer(serializers.ModelSerializer):
    fields = serializers.ListField(child=EnumField(enum_class=TemplateExportFieldChoices))

    class Meta:
        model = TemplateExport
        fields = ('fields',)


class TemplateExportRequestSerializer(serializers.Serializer):
    upload_template_id = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all())


class ImportTemplateSerializer(serializers.Serializer):
    file = serializers.PrimaryKeyRelatedField(queryset=File.objects.all())


class TemplateFieldResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateField
        fields = ('value', 'name', 'is_reusable')
