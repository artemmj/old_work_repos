INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',

    'corsheaders',
    'django_filters',
    'phonenumber_field',
    'drf_yasg',
    'rest_framework',
    'drf_extra_fields',
    'constance',
    'constance.backends.database',
    'storages',
    'ckeditor',

    'apps.user',
    'apps.file',
    'apps.channel',
    'apps.message',
]
