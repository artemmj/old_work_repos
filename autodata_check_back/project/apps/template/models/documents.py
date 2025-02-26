from django.db import models

from apps.helpers.models import UUIDModel


class TemplateDocumentsDetail(UUIDModel):
    sts = models.BooleanField('СТС', default=True)
    pts = models.BooleanField('ПТС', default=True)
    additional = models.BooleanField('Дополнительные документы', default=True)

    class Meta:
        verbose_name = 'Подробная настройка документов'
        verbose_name_plural = 'Подробные настройки документов'


class TemplateDocuments(UUIDModel):
    is_enable = models.BooleanField('Вкл/Выкл', default=True)
    detail = models.OneToOneField(
        TemplateDocumentsDetail,
        verbose_name='Подробная настройка документов',
        related_name='template_documents',
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField('Порядок', default=1)

    class Meta:
        verbose_name = 'Настройка документов'
        verbose_name_plural = 'Настройки документов'
