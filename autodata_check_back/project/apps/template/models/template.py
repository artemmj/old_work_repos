from typing import Final

from django.db import models

from apps.file.models import Image
from apps.helpers.models import CreatedModel, UUIDModel
from apps.template.models import (  # noqa: WPS235
    TemplateClient,
    TemplateCompleteness,
    TemplateDamage,
    TemplateDocuments,
    TemplateEquipment,
    TemplateLift,
    TemplatePaintwork,
    TemplatePhotos,
    TemplatePlace,
    TemplateSignatures,
    TemplateTechnical,
    TemplateTires,
    TemplateVideo,
)

_FIELD_MAX_LENGTH: Final = 200


class Template(UUIDModel, CreatedModel):
    title = models.CharField('Название', max_length=_FIELD_MAX_LENGTH)
    image = models.ForeignKey(
        Image,
        verbose_name='Фото',
        related_name='templates',
        on_delete=models.CASCADE,
        null=True,
    )
    user = models.ForeignKey(
        'user.User',
        verbose_name='Пользователь',
        related_name='templates',
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField('Активный шаблон', default=False)
    is_main = models.BooleanField('Основной шаблон', default=False)
    is_accreditation = models.BooleanField('Для аккредитации', default=False)

    # Настройки осмотра
    equipment = models.OneToOneField(
        TemplateEquipment,
        verbose_name='Комплектация',
        related_name='template',
        on_delete=models.CASCADE,
    )
    completeness = models.OneToOneField(
        TemplateCompleteness,
        verbose_name='Комплектность',
        related_name='template',
        on_delete=models.CASCADE,
    )
    documents = models.OneToOneField(
        TemplateDocuments,
        verbose_name='Документы',
        related_name='template',
        on_delete=models.CASCADE,
    )
    tires = models.OneToOneField(
        TemplateTires,
        verbose_name='Шины',
        related_name='template',
        on_delete=models.CASCADE,
    )
    photos = models.OneToOneField(
        TemplatePhotos,
        verbose_name='Фотографии',
        related_name='template',
        on_delete=models.CASCADE,
    )
    paintwork = models.OneToOneField(
        TemplatePaintwork,
        verbose_name='ЛКП',
        related_name='template',
        on_delete=models.CASCADE,
    )
    damage = models.OneToOneField(
        TemplateDamage,
        verbose_name='Повреждения',
        related_name='template',
        on_delete=models.CASCADE,
    )
    technical = models.OneToOneField(
        TemplateTechnical,
        verbose_name='Техническое состояние',
        related_name='template',
        on_delete=models.CASCADE,
    )
    lift = models.OneToOneField(
        TemplateLift,
        verbose_name='Осмотр на подъемнике',
        related_name='template',
        on_delete=models.CASCADE,
    )
    video = models.OneToOneField(
        TemplateVideo,
        verbose_name='Видео',
        related_name='template',
        on_delete=models.CASCADE,
    )
    place = models.OneToOneField(
        TemplatePlace,
        verbose_name='Место осмотра',
        related_name='template',
        on_delete=models.CASCADE,
    )
    client = models.OneToOneField(
        TemplateClient,
        verbose_name='Данные клиента',
        related_name='template',
        on_delete=models.CASCADE,
    )
    signatures = models.OneToOneField(
        TemplateSignatures,
        verbose_name='Подписи',
        related_name='template',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Шаблон осмотра'
        verbose_name_plural = 'Шаблоны осмотра'

    def __str__(self):
        return self.title
