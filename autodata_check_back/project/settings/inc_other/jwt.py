from datetime import timedelta

from ..common import env

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # noqa: WPS432

    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),
    'ROTATE_REFRESH_TOKENS': True,
    'SIGNING_KEY': env('JWT_SIGNING_KEY', str),
}
