from collections import OrderedDict

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'API_ID': ('', '', str),
    'API_HASH': ('', '', str),
    'PHONE': ('', '', str),
    'SESSION_KEY': ('', '', str),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'Настройки': ('API_ID', 'API_HASH', 'PHONE', 'SESSION_KEY'),
}
