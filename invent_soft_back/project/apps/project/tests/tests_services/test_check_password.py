import random

import pytest

from apps.project.services import ProjectCheckPasswordService

pytestmark = [pytest.mark.django_db]


def test_check_password(project):
    password = project.rmm_settings.password
    is_check_password = ProjectCheckPasswordService().process(project, password)

    assert is_check_password


def test_check_invalid_password(project):
    password = random.randrange(590, 1000)
    is_check_password = ProjectCheckPasswordService().process(project, str(password))

    assert is_check_password is False
