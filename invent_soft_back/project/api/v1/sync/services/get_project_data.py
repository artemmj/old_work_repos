from datetime import datetime

from api.v1.employee.serializers import EmployeeWideSerializer
from api.v1.project.serializers.rmm_settings import RMMSettingsReadSerializer
from api.v1.project.serializers.terminal_settings import TerminalSettingsReadSerializer
from api.v1.user.serializers import UserReadSerializer
from apps.employee.models import Employee
from apps.event.models import Event, TitleChoices
from apps.project.models import Project, RMMSettings, TerminalSettings


def generate_project_data(project_id: str):
    """Функция генерирует всю актуальную на текущий момент инфу по проекту."""
    project = Project.objects.get(pk=project_id)
    return_data = {
        'id': project.pk,
        'created_at': project.created_at,
        'title': project.title,
        'address': project.address,
        'manager': UserReadSerializer(project.manager).data,
    }

    rmm_settings = RMMSettings.objects.get(project=project)
    return_data['rmm_settings'] = RMMSettingsReadSerializer(rmm_settings).data

    terminal_settings = TerminalSettings.objects.get(project_id=project_id)
    return_data['terminal_settings'] = TerminalSettingsReadSerializer(terminal_settings).data

    employees = Employee.objects.filter(project=project, is_deleted=False)
    return_data['employees'] = EmployeeWideSerializer(employees, many=True).data

    Event.objects.create(
        project=project,
        title=TitleChoices.READY_TERMINAL_DB,
        comment=(
            'Подготовка терминальной БД: '
            f'была загружена информация о проекте '  # noqa: WPS326
            f'{project.title} в {datetime.now().strftime("%Y-%m-%d в %H:%M:%S")}'  # noqa: WPS326
        ),
    )

    return return_data
