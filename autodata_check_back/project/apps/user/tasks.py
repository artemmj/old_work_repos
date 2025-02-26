import os

from django.contrib.auth import get_user_model
from django.utils import timezone
from kombu import uuid
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font
from openpyxl.workbook import Workbook

from apps import app
from apps.user.models import RoleChoices

User = get_user_model()


@app.task
def users_export_excel(host: str) -> str:  # noqa: WPS210
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.column_dimensions['A'].width = 40
    ws.column_dimensions['B'].width = 50
    ws.column_dimensions['C'].width = 25
    ws.column_dimensions['D'].width = 30
    ws.column_dimensions['E'].width = 25
    cells = []
    coll_names = ['ID', 'ФИО', 'Номер телефона', 'Роли', 'Дата регистрации']
    for coll_name in coll_names:
        cell = WriteOnlyCell(ws, value=coll_name)
        cell.font = Font(bold=True)
        cells.append(cell)
    ws.append(cells)

    for user in User.objects.all():
        user_cells = [
            WriteOnlyCell(ws, value=str(user.id)),
            WriteOnlyCell(ws, value=f'{user.last_name} {user.first_name} {user.middle_name}'),  # noqa: WPS221
            WriteOnlyCell(ws, value=str(user.phone)),
            WriteOnlyCell(ws, value=', '.join([RoleChoices(role).label for role in user.roles])),
            WriteOnlyCell(ws, value=user.created_at.strftime('%Y-%m-%d %H:%M:%S')),
        ]
        ws.append(user_cells)

    dir_path = f'/media/users_export_excel/{timezone.now().strftime("%Y/%m/%d")}'  # noqa: WPS237
    filename = f'export_{uuid()}'
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    filepath = f'{dir_path}/{filename}.xlsx'
    wb.save(filepath)
    return f'{host}{filepath}'
