from django.core.exceptions import ValidationError
from django.db import models

from apps.helpers.model_fields import ChoiceArrayField
from apps.helpers.models import UUIDModel, enum_max_length
from apps.template.models.template_choices import TemplateExportFieldChoices, TemplateFieldChoices


class Template(UUIDModel):
    title = models.CharField('Название', max_length=200)
    field_separator = models.CharField('Разделитель полей', max_length=1)
    decimal_separator = models.CharField('Десятичный разделитель', max_length=1)
    fields = ChoiceArrayField(
        models.CharField(
            'Поле',
            max_length=enum_max_length(TemplateFieldChoices),
            choices=TemplateFieldChoices.choices,
        ),
        verbose_name='Список полей',
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Шаблон загрузки'
        verbose_name_plural = 'Шаблоны загрузки'

    def __str__(self):
        return self.title

    def clean(self):
        if len(self.fields) > 8:
            raise ValidationError('Невозможно выбрать более 8 пунктов')
        super().clean()


class TemplateExport(UUIDModel):
    title = models.CharField('Название', max_length=200)
    field_separator = models.CharField('Разделитель полей', max_length=1)
    decimal_separator = models.CharField('Десятичный разделитель', max_length=1)
    fields = ChoiceArrayField(
        models.CharField(
            'Поле',
            max_length=enum_max_length(TemplateExportFieldChoices),
            choices=TemplateExportFieldChoices.choices,
        ),
        verbose_name='Список полей',
    )
    storage_name = models.CharField('Код склада', max_length=200, null=True, blank=True)
    single_export = models.BooleanField('Поединичная выгрузка', default=False)
    zone_number_start = models.PositiveIntegerField(
        'Номер зоны, от',
        null=True,
        blank=True,
    )
    zone_number_end = models.PositiveIntegerField(
        'Номер зоны, до',
        null=True,
        blank=True,
    )
    is_products_find_by_code = models.BooleanField(
        'Товары, найденные по коду',
        help_text='Нужно ли добавлять в выгрузку товары, найденные по коду',
        default=False,
    )
    is_products_find_by_qr_code = models.BooleanField(
        'Товары, найденные по qr-коду',
        help_text='Нужно ли добавлять в выгрузку товары, найденные по qr-коду',
        default=False,
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Шаблон выгрузки'
        verbose_name_plural = 'Шаблоны выгрузки'

    def __str__(self):
        return self.title

    def clean(self):
        if len(self.fields) > 10:
            raise ValidationError('Невозможно выбрать более 10 пунктов')
        super().clean()
