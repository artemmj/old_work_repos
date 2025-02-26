import logging
import random

import requests

from settings.common import env

logger = logging.getLogger()


class SmsAPI:
    # https://smsc.ru/sys/send.php?login=<login>&psw=<password>&phones=<phones>&mes=<message>
    api_url = 'https://smsc.ru/sys/send.php'
    login = env('SMS_LOGIN')
    password = env('SMS_PASS')
    code = ''
    description_error = ''

    def __init__(self):  # noqa: D107
        self.session = requests.Session()
        self.session.headers['Host'] = 'smsc.ru'
        self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.session.headers['Content-Length'] = '78'
        self.session.headers['Connection'] = 'close'

    def send_sms(self, message, phone):
        try:  # noqa:  WPS229
            data = {   # noqa: WPS110
                'login': self.login,
                'psw': self.password,
                'phones': phone,
                'mes': message,
            }

            self.session.post(self.api_url, data=data)

        except Exception as e:
            logger.error(f'Ошибка при отправке смс - сообщение {message}, телефон {phone}. Exception - {e}')


def gen_code():
    digits = set(range(10))
    first = random.randint(1, 9)  # noqa: S311
    last_three = random.sample(digits - {first}, 3)
    return str(first) + ''.join(map(str, last_three))
