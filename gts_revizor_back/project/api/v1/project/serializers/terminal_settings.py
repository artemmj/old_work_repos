from datetime import datetime

from rest_framework import serializers

from apps.changelog.models import ChangeLog, ChangeLogActionType, ChangeLogModelType
from apps.event.models import Event, TitleChoices
from apps.helpers.serializers import EnumField
from apps.project.models import (
    CheckAMChoices,
    CheckDMChoices,
    IssuingTaskChoices,
    ProductNameChoices,
    RecalculationDiscrepancyChoices,
    TerminalSettings,
    UnknownBarcodeChoices,
)


class TerminalSettingsReadSerializer(serializers.ModelSerializer):
    issuing_task = EnumField(enum_class=IssuingTaskChoices)
    product_name = EnumField(enum_class=ProductNameChoices)
    unknown_barcode = EnumField(enum_class=UnknownBarcodeChoices)
    recalculation_discrepancy = EnumField(enum_class=RecalculationDiscrepancyChoices)
    check_dm = EnumField(enum_class=CheckDMChoices)
    check_am = EnumField(enum_class=CheckAMChoices)
    server_datetime = serializers.SerializerMethodField()

    class Meta:
        model = TerminalSettings
        fields = (
            'id',
            'server_datetime',
            'issuing_task',
            'length_barcode_pallets',
            'error_correction',
            'compliance_codes',
            'product_name',
            'unknown_barcode',
            'trimming_barcode',
            'recalculation_discrepancy',
            'suspicious_barcodes_amount',
            'check_dm',
            'check_am',
            'search_by_product_code',
            'manual_input_quantity',
            'is_scanning_of_weight_product',
            'password',
        )
        read_only_fields = ('id',)

    def get_server_datetime(self, instance):
        return datetime.now()


class TerminalSettingsUpdateSerializer(serializers.ModelSerializer):  # noqa: WPS338
    class Meta:
        model = TerminalSettings
        fields = (
            'id',
            'issuing_task',
            'length_barcode_pallets',
            'error_correction',
            'compliance_codes',
            'product_name',
            'unknown_barcode',
            'trimming_barcode',
            'recalculation_discrepancy',
            'suspicious_barcodes_amount',
            'check_dm',
            'check_am',
            'search_by_product_code',
            'manual_input_quantity',
            'is_scanning_of_weight_product',
            'password',
        )
        read_only_fields = ('id',)

    def _create_text_for_event(self, validated_data: dict, instance: TerminalSettings):
        comment = f'Изменены настройки терминала проекта {instance.project.title}, новые параметры:\r\n\r\n'
        for key, value in validated_data.items():
            _key = getattr(TerminalSettings, key).field.verbose_name  # noqa: WPS122
            comment += f'{_key} == {value}\r\n'
        return comment

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)

        ChangeLog.objects.create(
            project=obj.project,
            model=ChangeLogModelType.TERMINAL_SETTINGS,
            record_id=instance.pk,
            action_on_model=ChangeLogActionType.UPDATE,
            changed_data=validated_data,
        )

        Event.objects.create(
            project=obj.project,
            title=TitleChoices.TERMINAL_SETTINGS_UPDATE,
            comment=self._create_text_for_event(validated_data, instance),
        )
        return obj
