from datetime import timedelta

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(days=10),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}
