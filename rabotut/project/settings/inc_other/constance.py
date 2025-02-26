from collections import OrderedDict

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = OrderedDict(
    {
        'PHONE_CODE_KEY_TTL': (120, 'Количество секунд, в течении которых действует код', int),
        'SMS_CODE_IN_RESPONSE': (True, 'Отсылать код подтверждения в ответе', bool),
        'COUNT_SEND_SMS': (3, 'Разрешенное количество смс в сутки', int),
        'PHONE_CODE_COUNTER_TTL': (86400, 'Срок жизни счетчика в секундах', int),
    }
)

CONSTANCE_CONFIG_FIELDSETS = OrderedDict(
    {
        '1. Регистрация и авторизация мк': {
            'fields': (
                'PHONE_CODE_KEY_TTL',
                'COUNT_SEND_SMS',
                'SMS_CODE_IN_RESPONSE',
                'PHONE_CODE_COUNTER_TTL',
            ),
            'collapse': True,
        },
    }
)
