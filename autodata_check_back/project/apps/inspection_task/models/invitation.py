from django.db import models
from django_lifecycle import LifecycleModelMixin, hook

from apps.helpers.models import CreatedModel, UUIDModel


class Invitation(LifecycleModelMixin, UUIDModel, CreatedModel):
    inspector = models.ForeignKey(
        'user.User',
        verbose_name='Инспектор',
        related_name='invitations',
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        'inspection_task.InspectionTask',
        verbose_name='Задание на осмотр',
        related_name='invitations',
        on_delete=models.PROTECT,
    )
    is_accepted = models.NullBooleanField('Принял/Отклонил', default=None)

    class Meta:
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'

    @hook('after_update', when='is_accepted', is_now=True)
    def accept_invite(self):
        """Назначение инспектором после принятия приглашения."""
        from apps.inspection_task.services.assignment_inspector import AssignmentInspectorService  # noqa: WPS433, I001
        AssignmentInspectorService().process(self)
