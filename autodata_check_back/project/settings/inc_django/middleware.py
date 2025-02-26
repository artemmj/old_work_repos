from settings import DEBUG

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'apps.devices.middleware.DeviceMiddleware',
    'apps.organization.middleware.OrganizationMiddleware',
]

if DEBUG:
    MIDDLEWARE.append('querycount.middleware.QueryCountMiddleware')
