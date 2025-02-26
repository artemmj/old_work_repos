from ..common import env

EMAIL_HOST = env('EMAIL_HOST', str, None)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', str, None)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', str, None)
EMAIL_PORT = 465
EMAIL_USE_SSL = True
