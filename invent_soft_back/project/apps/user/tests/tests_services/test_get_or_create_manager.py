import pytest
from mixer.backend.django import mixer

from apps.project.models import User
from apps.user.services import GetOrCreateManagerService

pytestmark = [pytest.mark.django_db]


def test_create_manager():
    """Тест для проверки создания менеджера."""
    create_manager = {
        'id': '640ddae2-84ad-4e12-bb62-ada528d6da7a',
        'phone': '+79163042235',
        'username': '',
        'first_name': 'Чайник',
        'middle_name': 'Александрович',
        'last_name': 'Кипятков',
    }

    GetOrCreateManagerService(create_manager).process()

    assert User.objects.count() == 1
    assert User.objects.first().first_name == 'Чайник'


def test_get_manager():
    """Тест для проверки получения менеджера."""
    mixer.blend(
        User,
        phone='+79163042235',
        first_name='Чайник',
        middle_name='Александрович',
        last_name='Кипятков',
    )
    create_manager = {
        'id': '640ddae2-84ad-4e12-bb62-ada528d6da7a',
        'phone': '+79163042235',
        'username': '',
        'first_name': 'Лев',
        'middle_name': 'Иванович',
        'last_name': 'Яшин',
    }

    GetOrCreateManagerService(create_manager).process()

    assert User.objects.count() == 1
    assert User.objects.first().first_name == 'Чайник'
