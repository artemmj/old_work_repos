import os
from datetime import timedelta

from constance import config
from django.db.models import Q  # noqa: WPS347
from django.utils import timezone
from kombu import uuid
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font
from openpyxl.workbook import Workbook

from api.v1.inspection.serializers.inspection import InspectionsListSerializer
from apps import app
from apps.devices.tasks import send_push
from apps.inspection_task.models.search import InspectionTaskSearch
from apps.inspection_task.models.task import InspectionTask, InspectorTaskStatuses
from apps.inspection_task.services.issuing_invitations import IssuingInvitationsService
from apps.inspector.models.inspector import Inspector
from apps.notification.models.cant_get_task_non_requisite import CantGetTaskWithoutRequisiteNotification


@app.task
def issuing_invitations():
    """Выдача приглашений на задания."""
    for search_obj in InspectionTaskSearch.objects.filter(is_active=True, start_time_iter__lte=timezone.now()):
        IssuingInvitationsService(search_obj).process()


@app.task
def change_status_expired_tasks_to_draft():
    """Смена статуса просроченных заданий на черновик."""
    for inspection_task in InspectionTask.objects.filter(  # noqa: WPS352
        Q(
            status=InspectorTaskStatuses.INSPECTOR_SEARCH,
            inspection_task_search__start_time__lte=timezone.now() - timedelta(hours=config.INSPECTION_SEARCHING_TIME),
        ),
        Q(
            status=InspectorTaskStatuses.TASK_ACCEPTED,
            accepted_datetime__lte=timezone.now() - timedelta(hours=config.INSPECTION_TASK_ACTIVITY_TIME),
        )
        | Q(
            status__in=(
                InspectorTaskStatuses.INSPECTION_APPOINTED,
                InspectorTaskStatuses.INSPECTION_DATE_CONFIRMED,
            ),
            end_date__lt=timezone.now().date(),
        ),
    ).only('pk'):
        inspection_task.status = InspectorTaskStatuses.DRAFT
        inspection_task.save()


@app.task
def inspection_tasks_export_excel(host: str, organization_id: str = None) -> str:  # noqa: WPS210 WPS231
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.column_dimensions['A'].width = 40
    ws.column_dimensions['B'].width = 40
    ws.column_dimensions['C'].width = 40
    ws.column_dimensions['D'].width = 40
    ws.column_dimensions['E'].width = 40
    ws.column_dimensions['F'].width = 40
    ws.column_dimensions['G'].width = 40
    ws.column_dimensions['H'].width = 40
    cells = []
    coll_names = ['Авто', 'VIN', 'ФИО', 'Организация', 'Дата', 'Статус', 'Стоимость', 'Доступ']
    for coll_name in coll_names:
        cell = WriteOnlyCell(ws, value=coll_name)
        cell.font = Font(bold=True)
        cells.append(cell)
    ws.append(cells)

    inspection_tasks = InspectionTask.objects.all().exclude(status=InspectorTaskStatuses.DRAFT)
    if organization_id:
        inspection_tasks = inspection_tasks.filter(organization_id=organization_id)

    for inspection_task in inspection_tasks:
        for inspection in InspectionsListSerializer(inspection_task.inspections.all(), many=True).data:
            inspection_cells = [
                WriteOnlyCell(ws, value=inspection.get('brand_model')),
                WriteOnlyCell(ws, value=inspection.get('vin_code')),
                WriteOnlyCell(ws, value=inspection.get('fio')),
                WriteOnlyCell(ws, value=inspection.get('organization_title')),
                WriteOnlyCell(ws, value=inspection.get('task_created_at')),
                WriteOnlyCell(ws, value=inspection.get('task_status')),
                WriteOnlyCell(ws, value=inspection.get('price')),
                WriteOnlyCell(ws, value='Публичный' if inspection.get('is_public') else 'Приватный'),
            ]
            ws.append(inspection_cells)

    dir_path = f'/media/inspection_tasks_export_excel/{timezone.now().strftime("%Y/%m/%d")}'  # noqa: WPS237
    filename = f'export_{uuid()}'
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    filepath = f'{dir_path}/{filename}.xlsx'
    wb.save(filepath)
    return f'{host}{filepath}'


@app.task
def send_warnings_without_requisite_inspectors():
    """Расслыка пуш уведомлений инспекторам, прошедшим аккредитацию, но не заполнившим реквизиты."""
    for inspector in Inspector.objects.filter(requisite__isnull=True):
        notification = CantGetTaskWithoutRequisiteNotification.objects.create(
            user=inspector.user,
            message=config.CANT_GET_TASK_WITHOUT_REQUISITE,
        )
        send_push.delay(
            str(inspector.user_id),
            config.CANT_GET_TASK_WITHOUT_REQUISITE,
            {
                'push_type': 'CantGetTaskWithoutRequisiteNotification',
                'notification_id': str(notification.id),
            },
        )
