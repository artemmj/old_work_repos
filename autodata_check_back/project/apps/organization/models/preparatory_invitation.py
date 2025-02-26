from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.models import CreatedModel, UUIDModel
from apps.organization.models.organization import Organization


class PreparatoryInvitation(UUIDModel, CreatedModel):
    is_active = models.BooleanField('Активно', default=True)
    phone = PhoneNumberField('Номер телефона', help_text='Пример, +79510549236')
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='preparatory_invs',
    )

    class Meta:
        verbose_name = 'Предварительное приглашение по номеру'
        verbose_name_plural = 'Предварительные приглашения по номеру'
        constraints = [
            models.UniqueConstraint(
                fields=['phone', 'organization'],
                condition=models.Q(is_active=True),
                name='unique_phone_org',
            ),
        ]
