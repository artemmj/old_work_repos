from django.core.management.base import BaseCommand, CommandError

from ...models import User


class Command(BaseCommand):
    help = 'Создание пользователя с админскими правами'

    def add_arguments(self, parser):
        parser.add_argument('last_name', type=str, help='Фамилия')
        parser.add_argument('first_name', type=str, help='Имя')
        parser.add_argument('middle_name', type=str, help='Отчество')
        parser.add_argument('phone', type=str, help='Телефон')
        parser.add_argument('password', type=str, help='Пароль')

    def handle(self, *args, **kwargs):  # noqa: WPS231
        try:  # noqa: WPS229
            last_name = kwargs['last_name']
            first_name = kwargs['first_name']
            middle_name = kwargs['middle_name']
            phone = kwargs['phone']
            password = kwargs['password']

            middle_name = decode_surrogate(middle_name)
            first_name = decode_surrogate(first_name)
            last_name = decode_surrogate(last_name)
            password = decode_surrogate(password)

            user = User.objects.create(phone=phone, last_name=last_name, first_name=first_name, middle_name=middle_name)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            print('Создан администратор')  # noqa: T201 WPS421
        except Exception as e:
            raise CommandError(e)


def decode_surrogate(text):
    return text.encode('utf-8', 'surrogateescape').decode('utf-8')
