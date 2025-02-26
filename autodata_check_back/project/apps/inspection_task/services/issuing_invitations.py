from typing import List, Union

from constance import config
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Count, Min, Q, QuerySet  # noqa: WPS347

from apps.devices.tasks import send_push
from apps.helpers.services import AbstractService
from apps.inspection.models.inspection import StatusChoices
from apps.inspection_task.models.invitation import Invitation
from apps.inspection_task.models.search import InspectionTaskSearch
from apps.inspection_task.services.deactivate_searching import DeactivateSearchingService
from apps.inspection_task.services.next_level_searching import NextLevelSearchingService
from apps.inspector.models import Inspector
from apps.notification.models import TaskInvitationNotification


class IssuingInvitationsService(AbstractService):  # noqa: D107, WPS338
    """Сервиса подбора подходящих инспекторов и выдачи приглашений."""

    def __init__(self, search_obj: InspectionTaskSearch):  # noqa: D107
        self.search_obj = search_obj

    def _get_inspectors(self):
        """Получаем инспекторов с кол-вом осмотров равным уровню объекта поиска задания."""
        return Inspector.objects.filter(
            radius__gte=Distance('city__location', self.search_obj.task.address.location) / 1000,
        ).annotate(
            inspections_count=Count('user__inspections', filter=Q(user__inspections__status=StatusChoices.COMPLETE)),
        ).filter(
            inspections_count__gte=self.search_obj.level,
        ).exclude(
            user=self.search_obj.task.author, requisite__isnull=False,
        )

    def _get_min_inspections_count(self, inspectors: Union[QuerySet, List[Inspector]]):
        """Получаем минимальное кол-во осмотров из набора найденных инспекторов."""
        return inspectors.aggregate(min_inspections_count=Min('inspections_count'))['min_inspections_count']

    def _create_invitations(self, inspectors: Union[QuerySet, List[Inspector]], min_inspections_count: int):  # noqa: WPS210 E501
        """Создание приглашений инспекторам."""
        inspectors = inspectors.filter(
            inspections_count=min_inspections_count,
        ).values_list('user', flat=True).distinct()
        invitations = [
            Invitation(inspector_id=i, task=self.search_obj.task)
            for i in inspectors
            if not Invitation.objects.filter(inspector_id=i, task=self.search_obj.task).exists()
        ]
        invitations = Invitation.objects.bulk_create(invitations)
        for i in invitations:
            nmessage = config.ASSIGNING_INSPECTION_TO_INSPECTOR
            for task_car in i.task.inspection_task_cars.all():
                brand = task_car.brand.title
                model = task_car.model.title
                start_date = task_car.task.start_date
                end_date = task_car.task.end_date
                address = task_car.task.address
                nmessage += '\r\n'.join([
                    f'\r\nМарка: {brand}',
                    f'Модель: {model}',
                    f'Вин код: {task_car.vin_code}',
                    f'Дата начала осмотра: {start_date}',
                    f'Дата конца осмотра: {end_date}',
                    f'Адрес: {address}',
                ])

            notification = TaskInvitationNotification.objects.create(
                user=i.inspector,
                message=nmessage,
                inspection_task_invitation=i,
            )

            push_data = {
                'push_type': 'TaskInvitationNotification',
                'inspection_task_invitation': str(i.id),
                'notification_id': str(notification.id),
            }
            send_push(str(i.inspector_id), config.ASSIGNING_INSPECTION_TO_INSPECTOR, push_data)

    def _deactivate_search_obj(self):
        """Выключение объекта поиска."""
        DeactivateSearchingService(self.search_obj).process()

    def _next_level_search_obj(self):
        """Выставление объекту поиска новых уровня и времени."""
        NextLevelSearchingService(self.search_obj).process()

    def process(self):
        inspectors = self._get_inspectors()
        min_inspections_count = self._get_min_inspections_count(inspectors)
        if min_inspections_count is not None:
            self._create_invitations(inspectors, min_inspections_count)
            self._next_level_search_obj()
        else:
            self._deactivate_search_obj()
