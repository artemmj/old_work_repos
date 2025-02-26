from django.db import models


class OrderFrequencyTypes(models.TextChoices):
    EVERY_VISIT = 'every_visit', 'каждый день'  # noqa: WPS115
    ONCE = 'once', 'однократно'  # noqa: WPS115
