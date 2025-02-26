import os
from secrets import token_urlsafe

from django.utils import timezone
from openpyxl import Workbook

from apps import app
from apps.event.models import Event, TitleChoices
from apps.template.models import Template, TemplateExport


@app.task
def export_template(template_id: str, host: str, descr: str) -> str:
    if descr == 'template':
        template = Template.objects.get(pk=template_id)
    elif descr == 'export_template':
        template = TemplateExport.objects.get(pk=template_id)

    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    for field in Template._meta.get_fields():  # noqa: WPS437
        if field.name in ('id', 'projects'):  # noqa: WPS510
            continue
        field_value = getattr(template, field.name)
        if isinstance(field_value, list):
            field_value = ','.join(field_value)
        ws.append([field.name, field_value])

    date = timezone.now().strftime('%Y/%m/%d')
    random_string = token_urlsafe(10)
    dirpath = f'/media/upload/{date}/'
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    filepath = f'{dirpath}Шаблон_{template.title}_{random_string}.xlsx'
    wb.save(filepath)

    Event.objects.create(
        title=TitleChoices.EXPORT_TEMPLATE,
        comment=f'Был выгружен шаблон в файл Шаблон_{template.title}_{random_string}.xlsx',
    )

    return f'{host}{filepath}'
