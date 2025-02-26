from settings.common import env

ARKETA_API_URL = env('ARKETA_API_URL', str)
ARKETA_X_API_KEY = env('ARKETA_X_API_KEY', str, None)
