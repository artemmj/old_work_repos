from django.db import models

from apps.helpers.models import UUIDModel, enum_max_length
from apps.project.models.terminal_settings_choices import (
    CheckAMChoices,
    CheckDMChoices,
    IssuingTaskChoices,
    ProductNameChoices,
    RecalculationDiscrepancyChoices,
    UnknownBarcodeChoices,
)


class TerminalSettings(UUIDModel):
    project = models.OneToOneField(
        'project.Project', verbose_name='Проект', related_name='terminal_settings', on_delete=models.CASCADE,
    )
    issuing_task = models.CharField(
        'Выдача задания для УК',
        max_length=enum_max_length(IssuingTaskChoices),
        choices=IssuingTaskChoices.choices,
        default=IssuingTaskChoices.LEAST_LOADED_USER,
    )
    length_barcode_pallets = models.PositiveSmallIntegerField('Длина ШК Паллеты', default=0)
    error_correction = models.NullBooleanField('Исправление ошибок', default=False)
    compliance_codes = models.CharField(
        'Коды соответствия ШК х5',
        max_length=100,
        default='0-000;1-770;2-780,3-020;4-021;5-022;6-023;7-024;8-025;9-026',
    )
    product_name = models.CharField(
        'Наименование товара',
        max_length=enum_max_length(ProductNameChoices),
        choices=ProductNameChoices.choices,
        default=ProductNameChoices.BY_PRODUCT_CODE,
    )
    unknown_barcode = models.CharField(
        'Неизвестный штрих-код',
        max_length=enum_max_length(UnknownBarcodeChoices),
        choices=UnknownBarcodeChoices.choices,
        default=UnknownBarcodeChoices.DISALLOW,
    )
    trimming_barcode = models.PositiveSmallIntegerField(
        'Обрезка штрих-кода с начала и с конца', default=0,
    )
    recalculation_discrepancy = models.CharField(
        'Пересчет при расхождении',
        max_length=enum_max_length(RecalculationDiscrepancyChoices),
        choices=RecalculationDiscrepancyChoices.choices,
        default=RecalculationDiscrepancyChoices.SCAN,
    )
    suspicious_barcodes_amount = models.PositiveSmallIntegerField(
        'Подозрительное кол-во для ШК', default=15,
    )
    check_dm = models.CharField(
        'Проверка DM',
        max_length=enum_max_length(CheckDMChoices),
        choices=CheckDMChoices.choices,
        default=CheckDMChoices.WITHOUT_DM_CHECK,
    )
    check_am = models.CharField(
        'Проверка АМ',
        max_length=enum_max_length(CheckAMChoices),
        choices=CheckAMChoices.choices,
        default=CheckAMChoices.WITHOUT_AM_CHECK,
    )
    search_by_product_code = models.BooleanField('Поиск по коду товара', default=False)
    manual_input_quantity = models.BooleanField('Ручной ввод кол-ва', default=False)
    is_scanning_of_weight_product = models.BooleanField('Сканирования весового товара', default=False)
    password = models.CharField('Пароль редактирования', max_length=10, default='7467253')

    class Meta:
        verbose_name = 'Настройки параметров терминала'
        verbose_name_plural = 'Настройки параметров терминала'

    def __str__(self):
        return f'Настройки параметров терминала проекта {self.project.title}'
