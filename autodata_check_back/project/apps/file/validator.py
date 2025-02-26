import imghdr

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageExtensionValidator:
    def __init__(self, allowed_extensions):  # noqa: D107
        allowed_extensions = [allowed_extension.lower() for allowed_extension in allowed_extensions]
        self.allowed_extensions = allowed_extensions

    def __call__(self, in_memory_file):
        _extension = imghdr.what(in_memory_file)

        if not _extension:
            _extension = in_memory_file.name.split('.')[-1]

        if _extension not in self.allowed_extensions:
            raise ValidationError(
                f'Расширение файла не является допустимым. Допустимые расширения: {self.allowed_extensions}',
            )
