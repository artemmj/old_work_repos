from constance import config
from django.db import models
from django_lifecycle import LifecycleModelMixin, hook

from apps.devices.tasks import send_push
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.inspector_accreditation.services import AccreditationCreateInspectorService
from apps.notification.models.accr_request_new_fixes import InspectorAccrNewFixesNotification
from apps.notification.models.accr_succesfully_complete import InspectorAccrSuccCompleteNotification
from apps.template.models import Template


class StatusChoices(models.TextChoices):
    DRAFT = 'draft', 'Черновик'
    DISPATCHER_CHECK = 'dispatcher_check', 'На проверке у диспетчера'
    TROUBLESHOOTING = 'troubleshooting', 'Устранение недочетов'
    INSPECTION_ACCEPTED = 'inspection_accepted', 'Осмотр принят'


class AccreditationInspection(LifecycleModelMixin, UUIDModel, CreatedModel):
    address = models.ForeignKey(
        'address.Address',
        verbose_name='Адрес',
        related_name='accreditation_inspections',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.CharField(
        'Статус осмотра',
        max_length=enum_max_length(StatusChoices),
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )
    template = models.ForeignKey(
        Template,
        verbose_name='Шаблон осмотра',
        related_name='accreditation_inspections',
        on_delete=models.SET_NULL,
        null=True,
    )
    comment = models.TextField('Комментарий', null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Осмотр в заявке на аккредитацию инспектора'
        verbose_name_plural = 'Осмотры в заявках на аккредитацию инспекторов'

    def __str__(self):
        return f'{self.id}'

    @hook('after_update', when='status', has_changed=True, is_now=StatusChoices.INSPECTION_ACCEPTED)
    def create_inspector(self):
        accreditation_request = self.accreditation_requests.first()
        AccreditationCreateInspectorService(accreditation_request).process()

    @hook('after_update', when='status', has_changed=True)
    def after_update_status(self):  # noqa: WPS213 WPS231
        if self.status == StatusChoices.TROUBLESHOOTING:
            notification = InspectorAccrNewFixesNotification.objects.create(
                user=self.accreditation_requests.first().user,
                message=config.INSPECTOR_ACCR_NEW_FIXES,
                accreditation_inspection=self,
            )
            push_data = {
                'push_type': 'InspectorAccrNewFixesNotification',
                'accreditation_inspection': str(self.id),
                'notification_id': str(notification.id),
                'brand': self.car.brand.title if self.car else None,
                'model': self.car.model.title if self.car else None,
                'vin': self.car.vin_code if self.car else None,
            }
            send_push.delay(
                str(self.accreditation_requests.first().user_id),
                config.INSPECTOR_ACCR_NEW_FIXES,
                push_data,
            )
        elif self.status == StatusChoices.INSPECTION_ACCEPTED:
            notification = InspectorAccrSuccCompleteNotification.objects.create(
                user=self.accreditation_requests.first().user,
                message=config.INSPECTOR_ACCR_SUCC_COMPLETE,
                accreditation_inspection=self,
            )
            push_data = {
                'push_type': 'InspectorAccrSuccCompleteNotification',
                'accreditation_inspection': str(self.id),
                'notification_id': str(notification.id),
                'brand': self.car.brand.title if self.car else None,
                'model': self.car.model.title if self.car else None,
                'vin': self.car.vin_code if self.car else None,
            }
            send_push.delay(
                str(self.accreditation_requests.first().user_id),
                config.INSPECTOR_ACCR_SUCC_COMPLETE,
                push_data,
            )
