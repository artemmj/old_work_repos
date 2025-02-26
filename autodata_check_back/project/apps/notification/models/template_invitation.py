from django.db import models

from apps.notification.models import BaseNotification


class TemplateInvitationNotification(BaseNotification):
    template_invitation = models.ForeignKey(
        'template.TemplateInvitation',
        verbose_name='Приглашение принять шаблон',
        related_name='template_invitation_notifications',
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(
        to='organization.Organization',
        on_delete=models.CASCADE,
        related_name='template_invitation_notifications',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о принятии шаблона'
        verbose_name_plural = 'Уведомления о принятии шаблона'

    def __str__(self):
        return str(self.id)
