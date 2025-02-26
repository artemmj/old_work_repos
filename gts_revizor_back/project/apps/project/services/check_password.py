from apps.helpers.services import AbstractService
from apps.project.models import Project


class ProjectCheckPasswordService(AbstractService):
    """Сервис проверки пароля, заданного для проекта"""

    def process(self, project: Project, password: str) -> bool:
        """
        :param project: проект
        :param password: пароль
        """
        if not project.rmm_settings.password or (  # noqa: WPS337, WPS531, WPS408
            project.rmm_settings.password and project.rmm_settings.password == password
        ):
            return True
        return False
