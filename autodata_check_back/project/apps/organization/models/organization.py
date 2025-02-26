from typing import Final

from django.db import models
from django_lifecycle import LifecycleModelMixin, hook

from apps.dadata.services import DadataFindByINNService
from apps.helpers.inn_validator import inn_validator
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length

_FIELD_MAX_LENGTH: Final = 150
_FIELD_KPP_LENGTH: Final = 9
_FIELD_INN_LENGTH: Final = 12
_FIELD_OGRN_LENGTH: Final = 13
_FIELD_OGRNIP_LENGTH: Final = 15
_FIELD_ADDRESS_LENGTH: Final = 500
_FIELD_BALANCE_LENGTH: Final = 19


class TypeOrganizationChoices(models.TextChoices):
    LEGAL = 'legal', 'Юридическое лицо'  # noqa:  WPS115
    INDIVIDUAL = 'individual', 'Индивидуальный предприниматель'  # noqa:  WPS115


class Organization(LifecycleModelMixin, UUIDModel, CreatedModel):
    title = models.CharField('Название организации', max_length=_FIELD_MAX_LENGTH, null=True, blank=True)
    legal_title = models.CharField(
        'Юридическое название организации',
        max_length=_FIELD_MAX_LENGTH,
        null=True,
        blank=True,
    )
    inn = models.CharField(
        'ИНН',
        validators=[inn_validator],
        max_length=_FIELD_INN_LENGTH,
        null=True,
        blank=True,
    )
    kpp = models.CharField('КПП', max_length=_FIELD_KPP_LENGTH, null=True, blank=True)
    ogrn = models.CharField('ОГРН', max_length=_FIELD_OGRN_LENGTH, null=True, blank=True)
    ogrnip = models.CharField('ОГРНИП', max_length=_FIELD_OGRNIP_LENGTH, null=True, blank=True)
    address = models.CharField('Юридический адрес', max_length=_FIELD_ADDRESS_LENGTH, null=True, blank=True)
    type = models.CharField(
        'Тип организации',
        max_length=enum_max_length(TypeOrganizationChoices),
        choices=TypeOrganizationChoices.choices,
        default=TypeOrganizationChoices.INDIVIDUAL,
    )
    balance = models.DecimalField('Баланс', max_digits=_FIELD_BALANCE_LENGTH, decimal_places=2, default=0)
    users = models.ManyToManyField(
        'user.User',
        verbose_name='Пользователи',
        related_name='organizations',
        through='Membership',
    )
    is_active = models.BooleanField('Вкл/Выкл', default=True)
    self_inspection_price = models.DecimalField(
        'Цена за самостоятельный осмотр',
        max_digits=_FIELD_BALANCE_LENGTH,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.title if self.title else str(self.id)

    def owner(self):
        from apps.organization.models import MembershipRoleChoices  # noqa: WPS433
        return self.users.filter(membership__role=MembershipRoleChoices.OWNER).first() or '-'

    owner.short_description = 'Владелец'

    @hook('after_create')
    def after_create(self):
        if self.inn:
            from apps.organization.services.update_organization import UpdateOrganizationByDadataService  # noqa: WPS433
            dadata_response = DadataFindByINNService().process(self.inn)
            if dadata_response:
                UpdateOrganizationByDadataService(self, dadata_response).process()
                self.save()

    @hook('before_update', when='inn', has_changed=True)
    def before_update_inn(self):
        from apps.organization.services.update_organization import UpdateOrganizationByDadataService  # noqa: WPS433
        dadata_response = DadataFindByINNService().process(self.inn)
        if dadata_response:
            UpdateOrganizationByDadataService(self, dadata_response).process()
