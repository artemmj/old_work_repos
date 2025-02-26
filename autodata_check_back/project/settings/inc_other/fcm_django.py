from firebase_admin import credentials, initialize_app

from settings.common import env

GOOGLE_APPLICATION_CREDENTIALS = env('GOOGLE_APPLICATION_CREDENTIALS', str, None)
CERT = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
FIREBASE_APP = initialize_app(CERT)

FCM_DJANGO_SETTINGS = {
    'FCM_SERVER_KEY': env('FCM_SERVER_KEY', str, None),
    'ONE_DEVICE_PER_USER': False,
    'DELETE_INACTIVE_DEVICES': True,
    'APP_VERBOSE_NAME': 'FCM Django',
    'UPDATE_ON_DUPLICATE_REG_ID': True,
}
