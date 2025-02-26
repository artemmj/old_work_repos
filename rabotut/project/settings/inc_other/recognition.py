from settings.common import env

RECOGNITION_API_URL = env('RECOGNITION_API_URL', str)
RECOGNITION_API_TOKEN = env('RECOGNITION_API_TOKEN', str)
FACE_RECOGNITION_DOMAIN = env('FACE_RECOGNITION_DOMAIN', str, 'https://api-face-recognition.arktech.ai/')

PASSPORT_RECOGNITION_FULL_URL = env(
    'PASSPORT_RECOGNITION_FULL_URL',
    str,
    'http://d2-ark-smart01.ark.info/ArktechRecognition/v1/recognition/recognize/',
)
PASSPORT_RECOGNITION_CLIENT_ID = env('PASSPORT_RECOGNITION_CLIENT_ID', str, 'Arktech-recognition')
PASSPORT_RECOGNITION_AUTH_TOKEN = env('PASSPORT_RECOGNITION_AUTH_TOKEN', str, '')
