from django.apps import AppConfig
from django.db.models.signals import post_save


class TemplateConfig(AppConfig):
    name = 'apps.template'
    verbose_name = 'Шаблон осмотра'

    def ready(self):
        from .models import Template  # noqa: WPS433
        from .signals import deactivate_templates_signal  # noqa: WPS433

        post_save.connect(deactivate_templates_signal, sender=Template)
