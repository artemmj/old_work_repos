import pathlib
from secrets import token_urlsafe

from django.db import models
from django.utils import timezone

from apps.file.validator import ImageExtensionValidator
from apps.helpers.models import CreatedModel, DeletedModel, ForceCleanModel, UUIDModel


def directory_path(instance, filename):
    """Генерирует рандомную url safe строку в зависимости от текущей даты."""
    date = timezone.now().strftime('%Y/%m/%d')
    random_string = token_urlsafe(10)
    extension = pathlib.Path(filename).suffix
    return f'upload/{date}/{random_string}{extension}'


class File(UUIDModel, CreatedModel, DeletedModel):  # noqa: WPS110
    file = models.FileField(upload_to=directory_path)  # noqa: WPS110

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.file.url


class Image(UUIDModel, CreatedModel, DeletedModel, ForceCleanModel):
    image = models.FileField(
        upload_to=directory_path,
        validators=[ImageExtensionValidator(allowed_extensions=('jpg', 'jpeg', 'webp', 'png', 'gif'))],
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.image.url
