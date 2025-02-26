# https://github.com/encode/django-rest-framework

REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S.%f%z',
    'DATE_FORMAT': '%Y-%m-%d',
    'TIME_FORMAT': '%H:%M',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (),
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_FILTER_BACKENDS': (
        'apps.helpers.filters.CustomDjangoFilterBackend',
        'apps.helpers.filters.SearchFilterWithoutDistinct',
    ),
    'DEFAULT_THROTTLE_RATES': {},
    'OVERIDE_THROTTLE_RATES': {},
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
}

DRF_STANDARDIZED_ERRORS = {
    'EXCEPTION_FORMATTER_CLASS': 'apps.helpers.exceptions.CustomExceptionFormatter',
}
