import os
from secrets import token_urlsafe

from django.utils import timezone
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font

from api.v1.employee.serializers import EmployeeReadSerializer
from apps import app
from apps.employee.models import Employee


@app.task
def export_employees(project_id: str, host: str) -> str:
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    ws.column_dimensions['A'].width = 15
    ws.column_dimensions['B'].width = 25
    ws.column_dimensions['C'].width = 30
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 15
    ws.column_dimensions['H'].width = 15
    ws.column_dimensions['I'].width = 20
    cells = []
    for coll_name in [  # noqa:  WPS352, WPS317, WPS335
        'Номер', 'ФИО', 'Роли', 'Норма', 'С.Скан',
        'С.УК', 'А.Скан', 'А.УК', 'Сотрудник склада',
    ]:
        cell = WriteOnlyCell(ws, value=coll_name)
        cell.font = Font(bold=True)
        cells.append(cell)
    ws.append(cells)

    employees = Employee.objects.filter(project_id=project_id)
    employees = EmployeeReadSerializer(employees, many=True).data
    for employee in employees:
        ws.append([
            employee['serial_number'],
            employee['username'],
            ','.join([item['name'] for item in employee['roles']]),
            employee['norm'],
            employee['counter_scan'],
            employee['controller'],
            employee['auditor'],
            employee['auditor_controller'],
            employee['storage'],
        ])

    date = timezone.now().strftime('%Y/%m/%d')
    random_string = token_urlsafe(10)
    dirpath = f'/media/upload/{date}/'
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    filepath = f'{dirpath}Отчет_по_сотрудникам_{random_string}.xlsx'
    wb.save(filepath)
    return f'{host}{filepath}'
