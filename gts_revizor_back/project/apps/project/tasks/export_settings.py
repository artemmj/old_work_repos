import os
from secrets import token_urlsafe

from django.utils import timezone
from openpyxl import Workbook

from apps import app
from apps.project.models import Project, RMMSettings, TerminalSettings


@app.task
def export_settings(project_id: str, host: str) -> str:  # noqa: WPS231
    project = Project.objects.get(id=project_id)
    rmm_settings_obj = RMMSettings.objects.get(project_id=project_id)
    terminal_settings_obj = TerminalSettings.objects.get(project_id=project_id)

    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    data = {model: model._meta.get_fields() for model in [RMMSettings, TerminalSettings]}  # noqa: WPS437, WPS335
    for model, fields in data.items():
        for field in fields:
            if field.name in ('id', 'project'):  # noqa: WPS510
                continue
            if model == RMMSettings:
                field_value = getattr(rmm_settings_obj, field.name)
            else:
                field_value = getattr(terminal_settings_obj, field.name)
            if isinstance(field_value, bool):
                field_value = str(field_value)
            ws.append([field.name, field_value])

    date = timezone.now().strftime('%Y/%m/%d')
    random_string = token_urlsafe(10)
    dirpath = f'/media/upload/{date}/'
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    title = project.title.replace('/', ' ')
    filepath = f'{dirpath}Настройки_Проекта_{title}_{random_string}.xlsx'
    wb.save(filepath)
    return f'{host}{filepath}'
