from itertools import islice
from typing import Dict, Union

from openpyxl import load_workbook

from apps import app
from apps.event.models import Event, TitleChoices
from apps.file.models import File
from apps.project.models import Project, RMMSettings, TerminalSettings


def update_settings(instance: Union[RMMSettings, TerminalSettings], data: Dict):
    for attr, value in data.items():
        setattr(instance, attr, value)
    instance.save()


@app.task
def import_settings(file: File, project: Project) -> Dict:
    file = File.objects.get(id=file).file.path
    project = Project.objects.get(id=project)
    settings = []
    rmm_settings_data = {}
    terminal_settings_data = {}

    event_comment_data = 'Загружены настройки:\n\n'

    wb = load_workbook(filename=file)
    sheet = wb.worksheets[0]
    errors = []
    try:  # noqa: WPS229
        for i, row in enumerate(islice(sheet.rows, 0, None)):
            name, value = row[:2]
            if i in range(0, 4):
                rmm_settings_data[name.value] = value.value
                settings.append({project.rmm_settings: rmm_settings_data})
            else:
                terminal_settings_data[name.value] = value.value
                settings.append({project.terminal_settings: terminal_settings_data})

            event_comment_data += f'{name.value} == {value.value}\n\n'

        Event.objects.create(project=project, title=TitleChoices.PROJECT_SETTINGS_LOAD, comment=event_comment_data)

        for item in settings:
            for instance, data in item.items():
                update_settings(instance, data)

    except Exception as e:
        errors.append(str(e))

    return {'errors': errors}
