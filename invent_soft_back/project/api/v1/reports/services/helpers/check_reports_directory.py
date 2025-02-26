import os

from django.conf import settings
from django.utils import timezone


def check_reports_directory() -> str:
    """Функция проверяет наличие директорий для репортов, создает при необходимости."""
    if not os.path.exists(f'{settings.MEDIA_ROOT}/reports'):
        os.mkdir(f'{settings.MEDIA_ROOT}/reports')

    date = timezone.now().strftime('%Y-%m-%d')
    if not os.path.exists(f'{settings.MEDIA_ROOT}/reports/{date}/'):
        os.mkdir(f'{settings.MEDIA_ROOT}/reports/{date}')

    return date
