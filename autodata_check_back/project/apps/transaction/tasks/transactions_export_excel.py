import os

from django.utils import timezone
from kombu import uuid
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font
from openpyxl.workbook import Workbook

from apps import app
from apps.transaction.models.organization import OrganizationTransaction


@app.task
def transactions_export_excel(host: str, organization_id: str) -> str:  # noqa: WPS210
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 50
    ws.column_dimensions['E'].width = 30
    ws.column_dimensions['F'].width = 50
    ws.column_dimensions['G'].width = 50
    cells = []
    coll_names = ['+/- сумма', 'Дата', 'Время', 'Организация', 'Пользователь', 'За задание', 'ID операции']
    for coll_name in coll_names:
        cell = WriteOnlyCell(ws, value=coll_name)
        cell.font = Font(bold=True)
        cells.append(cell)
    ws.append(cells)

    transactions = OrganizationTransaction.objects.all()
    if organization_id:
        transactions = transactions.filter(organization_id=organization_id)

    for trans in transactions:
        transaction_cells = [
            WriteOnlyCell(ws, value=trans.amount),
            WriteOnlyCell(ws, value=str(trans.created_at.date())),
            WriteOnlyCell(ws, value=str(trans.created_at.time())),
            WriteOnlyCell(ws, value=trans.organization.title),
            WriteOnlyCell(ws, value=f'{trans.user.first_name} {trans.user.last_name}'),  # noqa: WPS237
            WriteOnlyCell(ws, value=trans.get_operation_display()),
            WriteOnlyCell(ws, value=str(trans.pk)),
        ]
        ws.append(transaction_cells)

    dir_path = f'/media/transactions_export_excel/{timezone.now().strftime("%Y/%m/%d")}'  # noqa: WPS237
    filename = f'export_{uuid()}'
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    filepath = f'{dir_path}/{filename}.xlsx'
    wb.save(filepath)
    return f'{host}{filepath}'
