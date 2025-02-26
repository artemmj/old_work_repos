from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ...models import User


class Command(BaseCommand):
    help = 'Создание пользователя для замены удаленных'
    phone = settings.REMOTE_USER_PHONE

    def handle(self, *args, **kwargs):  # noqa: WPS110
        try:  # noqa: WPS229
            user = User.objects.create(
                email='remote@test.ru',
                phone=self.phone,
                first_name='Удален',
                last_name='Удален',
            )
            user.is_staff = False
            user.is_superuser = False
            user.save()
            print(f'Создан юзер для замены удаленных {self.phone}')  # noqa: T001, WPS421, T201
        except Exception as e:
            raise CommandError(e)
