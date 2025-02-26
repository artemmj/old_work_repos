import pytest
from mixer.backend.django import mixer

from apps.project.models import Project

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def project():
    return mixer.blend(Project)
