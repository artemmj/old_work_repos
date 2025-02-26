# flake8: noqa
import os

import environ

env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    SECRET_KEY=(str, ''),
    SENTRY_DSN=(str, ''),
    USING_S3_STORAGE=(bool, False),
)

SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..')

ROOT_URLCONF = 'apps.urls'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Django settings
from .inc_django.applications import *
from .inc_django.auth import *
from .inc_django.caches import *
from .inc_django.databases import *
from .inc_django.email import *
from .inc_django.languages import *
from .inc_django.logging import *
from .inc_django.media import *
from .inc_django.middleware import *
from .inc_django.security import *
from .inc_django.static import *
from .inc_django.templates import *
from .inc_django.tz import *
# 3-rd party tools
from .inc_other.arketa import *
from .inc_other.celery_config import *
from .inc_other.ckeditor import *
from .inc_other.constance import *
from .inc_other.cors import *
from .inc_other.drf import *
from .inc_other.fcm_django import *
from .inc_other.jwt import *
from .inc_other.recognition import *
from .inc_other.red_sms import *
from .inc_other.sentry_config import *
from .inc_other.swagger import *
