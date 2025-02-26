import os

from django.utils import timezone
from kombu import uuid
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font
from openpyxl.workbook import Workbook

from apps import app
from apps.inspection.models.inspection import StatusChoices
from apps.organization.models import Organization


@app.task
def organizations_export_excel_task(host: str) -> str:  # noqa: WPS210
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.column_dimensions['A'].width = 50
    ws.column_dimensions['B'].width = 50
    ws.column_dimensions['C'].width = 30
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 20
    ws.column_dimensions['F'].width = 50

    cells = []
    coll_names = [
        'Название',
        'ИНН',
        'Кол-во участников',
        'Цена за осмотр',
        'Кол-во осмотров',
        'Тарифный план',
    ]

    for coll_name in coll_names:
        cell = WriteOnlyCell(ws, value=coll_name)
        cell.font = Font(bold=True)
        cells.append(cell)
    ws.append(cells)

    for organization in Organization.objects.all():
        org_subs = organization.subscriptions.filter(is_active=True, end_datetime__gte=timezone.now()).exists()
        user_cells = [
            WriteOnlyCell(ws, value=organization.title),
            WriteOnlyCell(ws, value=organization.inn),
            WriteOnlyCell(ws, value=organization.users.count()),
            WriteOnlyCell(ws, value=organization.self_inspection_price),
            WriteOnlyCell(ws, value=organization.inspections.filter(status=StatusChoices.COMPLETE).count()),
            WriteOnlyCell(ws, value='Есть' if org_subs else 'Нет'),
        ]
        ws.append(user_cells)

    dir_path = f'/media/organizations_export_excel/{timezone.now().strftime("%Y/%m/%d")}'  # noqa: WPS237
    filename = f'export_{uuid()}'
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    filepath = f'{dir_path}/{filename}.xlsx'
    wb.save(filepath)
    return f'{host}{filepath}'
