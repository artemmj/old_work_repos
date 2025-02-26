from django.core.management.base import BaseCommand, CommandError

from ...models import User


class Command(BaseCommand):
    help = 'Создание пользователя с админскими правами'

    def handle(self, *args, **kwargs):  # noqa: WPS110
        try:  # noqa: WPS229
            user = User.objects.create(
                email='master_test@test.ru',
                phone='+79000000000',
                first_name='Мастер',
                last_name='Мастер',
            )
            user.is_staff = True
            user.is_superuser = True
            user.set_password('123')
            user.save()
            print('Создан админ +79000000000/123')  # noqa: T001 WPS421
        except Exception as e:
            raise CommandError(e)
