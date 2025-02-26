from django.core.management.base import BaseCommand, CommandError

from apps.user.models import User


class Command(BaseCommand):
    help = 'Создание пользователя с админскими правами'

    def handle(self, *args, **kwargs):  # noqa: WPS110
        try:  # noqa: WPS229
            user = User.objects.create(
                email='admin@admin.ru',
                phone='+79270000001',
                first_name='Admin',
                middle_name='Admin',
                last_name='Admin',
            )
            user.is_staff = True
            user.is_superuser = True
            user.set_password('123')
            user.save()
            print('Создан админ +79270000001/123')  # noqa: T001 WPS421, T201
        except Exception as e:
            raise CommandError(e)
