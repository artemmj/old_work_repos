from django.apps import AppConfig
from django.db.models.signals import post_save


class OrganizationConfig(AppConfig):
    name = 'apps.organization'
    verbose_name = 'Организация'

    def ready(self):
        from .models import Membership  # noqa: WPS433
        from .signals import deactivate_membership_signal  # noqa: WPS433

        post_save.connect(deactivate_membership_signal, sender=Membership)
