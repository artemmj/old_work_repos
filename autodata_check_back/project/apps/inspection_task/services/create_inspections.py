from constance import config

from api.v1.notification.serializers import (
    IssuingOrganizationInspectorNotificationSerializer,
    IssuingServiceInspectorNotificationSerializer,
)
from apps.devices.tasks import send_push
from apps.helpers.services import AbstractService
from apps.inspection_task.models.task import InspectionTask, InspectorTaskTypes
from apps.notification.models import IssuingOrganizationInspectorNotification, IssuingServiceInspectorNotification
from apps.template.models import Template


class CreateInspectionsService(AbstractService):
    """Сервис создает осмотр, создает авто."""

    def __init__(self, inspection_task: InspectionTask):  # noqa: D107
        self.inspection_task = inspection_task
        self.task_cars = inspection_task.inspection_task_cars.all()

    def process(self, *args, **kwargs):
        from apps.car.models.car import Car  # noqa: WPS433
        from apps.inspection.models.inspection import Inspection, InspectionTypes  # noqa: WPS433

        cars_info = []
        for task_car in self.task_cars:
            inspection_type = InspectionTypes.BY_TASK_WITH_ORGANIZATION_INSPECTOR
            template = self.inspection_task.inspector.templates.filter(is_active=True).first()

            if self.inspection_task.type == InspectorTaskTypes.FOR_SEARCH_INSPECTOR:
                inspection_type = InspectionTypes.BY_TASK
                template = Template.objects.filter(is_main=True, is_active=True).first()

            inspection = Inspection.objects.create(
                inspector=self.inspection_task.inspector,
                organization=self.inspection_task.organization,
                task=self.inspection_task,
                address=self.inspection_task.address,
                template=template,
                type=inspection_type,
            )
            Car.objects.create(
                category=task_car.category,
                brand=task_car.brand,
                model=task_car.model,
                vin_code=task_car.vin_code,
                unstandart_vin=task_car.unstandart_vin,
                inspection=inspection,
            )

            task_car.inspection = inspection
            task_car.save()

            cars_info.append({
                'vin_code': task_car.vin_code,
                'start_date': self.inspection_task.start_date,
                'end_date': self.inspection_task.end_date,
                'brand': task_car.brand.title,
                'model': task_car.model.title,
            })

        self._send_notification(cars_info=cars_info)

    def _send_notification(self, cars_info) -> None:  # noqa: WPS210
        if self.inspection_task.type == InspectorTaskTypes.FOR_SEARCH_INSPECTOR:
            return

        model = IssuingOrganizationInspectorNotification
        serializer = IssuingOrganizationInspectorNotificationSerializer
        message = config.ISSUING_ORG_INSPECTOR
        push_type = 'IssuingOrganizationInspectorNotification'

        notification = model.objects.create(
            user=self.inspection_task.inspector,
            message=self._generate_cars_string(message, cars_info),
            task=self.inspection_task,
        )
        serializer = serializer(notification)

        data = {
            'push_type': push_type,
            'notification_id': str(notification.id),
            'cars_info': serializer.data.get('cars_info'),
        }
        send_push.delay(str(self.inspection_task.inspector_id), message, data)

    def _generate_cars_string(self, message, cars_info) -> str:  # noqa: WPS210
        for car in cars_info:  # noqa: WPS519
            cbrand = car.get('brand')
            cmodel = car.get('model')
            cvin_code = car.get('vin_code')
            cstartdate = car.get('start_date')
            cenddate = car.get('end_date')

            message += '\r\n'  # noqa: WPS336
            message += '\r\n'.join([
                f'\r\nМарка: {cbrand}',
                f'Модель: {cmodel}',
                f'Вин код: {cvin_code}',
                f'Дата начала осмотра: {cstartdate}',
                f'Дата конца осмотра: {cenddate}',
            ])

        if self.inspection_task.type == InspectorTaskTypes.FOR_APPOINTMENT:
            amount = self.inspection_task.inspector_amount
            message += f'\r\nСтоимость: {amount}'  # noqa: WPS336

        return message
