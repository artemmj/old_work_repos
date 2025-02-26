import pathlib
from secrets import token_urlsafe

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django_lifecycle import LifecycleModelMixin, hook

from apps.file.validator import ImageExtensionValidator
from apps.helpers.models import CreatedModel, DeletedModel, ForceCleanModel, UUIDModel, enum_max_length


def directory_path(instance, filename):
    date = timezone.now().strftime('%Y/%m/%d')
    random_string = token_urlsafe(10)
    extension = pathlib.Path(filename).suffix
    return f'upload/{date}/{random_string}{extension}'


def directory_db_path(instance, filename):
    date_dir = timezone.now().strftime('%Y/%m/%d')
    date_filename = timezone.now().strftime('%Y_%m_%d')
    return f'export_db/{date_dir}/{date_filename}.json'


class File(UUIDModel, CreatedModel, DeletedModel):  # noqa: WPS110
    file = models.FileField(upload_to=directory_path)  # noqa: WPS110

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.file.path


class Image(UUIDModel, CreatedModel, DeletedModel, ForceCleanModel):
    image = models.FileField(
        upload_to=directory_path,
        validators=[ImageExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'webp', 'png', 'gif', 'pdf', 'svg'))],
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.image.url


class DBFile(LifecycleModelMixin, CreatedModel):
    file = models.FileField(    # noqa: WPS110
        upload_to=directory_db_path,
        validators=[FileExtensionValidator(allowed_extensions=('json',))],
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Файл БД'
        verbose_name_plural = 'Файлы БД'

    def __str__(self):
        return self.file.path

    @hook('after_create')
    def after_create(self):
        count = DBFile.objects.count()
        obj = DBFile.objects.last()   # noqa: WPS110
        if obj and count > 1:
            obj.file.delete(False)
            obj.delete()


class StaticFileType(models.TextChoices):
    AGREEMENT = 'agreement', 'Согласие на обработку перс. данных'
    PRIVACY_POLICY = 'privacy_policy', 'Политика конфиденциальности'
    TERMS_OF_USE = 'terms_of_use', 'Условия пользования'


class StaticFile(UUIDModel, CreatedModel):
    file = models.FileField(upload_to=directory_path)  # noqa: WPS110
    type = models.CharField(
        'Тип',
        choices=StaticFileType.choices,
        max_length=enum_max_length(StaticFileType),
        unique=True,
    )

    class Meta:
        verbose_name = 'Статический файл для апи'
        verbose_name_plural = 'Статические файлы для апи'

    def __str__(self):
        return self.file.path
