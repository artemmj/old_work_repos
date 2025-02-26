# flake8: noqa
from .common import *  # noqa

SITE_URL = env('SITE_URL')
ALLOWED_HOSTS = ['*']
DEBUG = True
SECRET_KEY = 'not-a-valid-secret-key'
