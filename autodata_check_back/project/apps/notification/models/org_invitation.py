from django.db import models

from apps.notification.models import BaseNotification


class OrganizationInvitationNotification(BaseNotification):
    org_invitation = models.ForeignKey(
        'organization.OrgInvitation',
        verbose_name='Приглашение на вступление в организацию',
        related_name='org_invitation_notifications',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Уведомление о приглашении вступить в организацию'
        verbose_name_plural = 'Уведомления о приглашении вступить в организацию'

    def __str__(self):
        return str(self.id)
