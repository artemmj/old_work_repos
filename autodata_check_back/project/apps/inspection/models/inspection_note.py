from django.db import models
from django_lifecycle import LifecycleModelMixin, hook

from apps.helpers.models import CreatedModel, UUIDModel
from apps.inspection.models.inspection import Inspection, StatusChoices


class InspectionNote(LifecycleModelMixin, UUIDModel, CreatedModel):
    text = models.TextField('Текст замечания')
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='notes')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Замечание по осмотру'
        verbose_name_plural = 'Замечания по осмотрам'

    @hook('after_create')
    def after_create(self):
        self.inspection.status = StatusChoices.TROUBLESHOOTING
        self.inspection.save()
