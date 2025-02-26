from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db.models import PointField
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook
from phonenumber_field.modelfields import PhoneNumberField

from apps.address.models import City
from apps.departments.models import Department
from apps.helpers.consts import CHAR_FIELD_LENGTH_150
from apps.helpers.managers import CustomFieldUserManager
from apps.helpers.models import UUIDModel, enum_max_length
from apps.projects.models import Project
from apps.regions.models import Region

from .doc_statuses import UserDocStatuses


class UserRoles(models.TextChoices):
    MASTER = 'master', 'Мастер'
    APPLICANT = 'applicant', 'Аппликант'
    APPLICANT_CONFIRMED = 'applicant_confirmed', 'Аппликант подтвержденный'
    CANDIDATE = 'candidate', 'Кандидат'
    EMPLOYEE = 'emoloyee', 'Сотрудник'
    SUPERVISOR = 'supervisor', 'Супервизор'
    DISMISSED = 'dismissed', 'Уволенный'


class User(LifecycleModelMixin, UUIDModel, AbstractUser):
    phone = PhoneNumberField('Номер телефона', unique=True, help_text='Пример, +79510549236')
    first_name = models.CharField('Имя', max_length=CHAR_FIELD_LENGTH_150, blank=True)
    last_name = models.CharField('Фамилия', max_length=CHAR_FIELD_LENGTH_150, blank=True)
    middle_name = models.CharField('Отчество', max_length=CHAR_FIELD_LENGTH_150, blank=True)
    email = models.EmailField('Адрес электронной почты', default='')
    username = models.CharField('Имя пользователя', max_length=CHAR_FIELD_LENGTH_150, blank=True)
    role = models.CharField(
        'Роль',
        max_length=enum_max_length(UserRoles),
        choices=UserRoles.choices,
        default=UserRoles.APPLICANT,
    )
    is_self_employed = models.BooleanField('Cамозанятой или нет, если null - то не известно', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name='Город', null=True, blank=True)
    department = models.ForeignKey(
        Department,
        verbose_name='Департамент',
        related_name='users',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    regions = models.ManyToManyField(
        Region,
        verbose_name='Регионы',
        related_name='users',
        blank=True,
    )
    projects = models.ManyToManyField(
        Project,
        verbose_name='Проекты',
        related_name='users',
        blank=True,
    )
    location = PointField(verbose_name='Местоположение', null=True, blank=True)
    doc_status = models.CharField(
        verbose_name='Общий статус документов пользователя',
        choices=UserDocStatuses.choices,
        max_length=enum_max_length(UserDocStatuses),
        default=UserDocStatuses.APPROVAL,
    )
    arketa_user_id = models.UUIDField('Id пользователя в аркете', null=True, blank=True)

    objects = CustomFieldUserManager(username_field_name='phone')  # noqa: WPS110

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ('date_joined',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.phone)

    def get_username(self):
        # for jwt_payload_handler
        return str(self.phone)

    @hook('after_update', when='phone', has_changed=True)
    def change_phone_in_arketa(self):
        from apps.arketa.tasks import change_user_phone_in_arketa  # noqa: WPS433
        if self.arketa_user_id:
            change_user_phone_in_arketa.delay(user_id=str(self.id), phone=str(self.phone))
