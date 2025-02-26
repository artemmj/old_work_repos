from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # noqa: WPS432

    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),
    'ROTATE_REFRESH_TOKENS': True,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'id',
    'UPDATE_LAST_LOGIN': True,
}
