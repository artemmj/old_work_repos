import json
from pathlib import Path

from firebase_admin import credentials, initialize_app

from settings.common import env

GOOGLE_APPLICATION_CREDENTIALS = env('FIREBASE_CONFIG', str, '/app/firebase_config.json')
if not Path(GOOGLE_APPLICATION_CREDENTIALS).exists():
    GOOGLE_APPLICATION_CREDENTIALS = json.loads(GOOGLE_APPLICATION_CREDENTIALS)
CERT = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
FIREBASE_APP = initialize_app(CERT)

FCM_DJANGO_SETTINGS = {
    'FCM_SERVER_KEY': env('FCM_SERVER_KEY', str, None),
    'ONE_DEVICE_PER_USER': False,
    'DELETE_INACTIVE_DEVICES': False,
    'APP_VERBOSE_NAME': 'Rabotut',
    'UPDATE_ON_DUPLICATE_REG_ID': True,
}
