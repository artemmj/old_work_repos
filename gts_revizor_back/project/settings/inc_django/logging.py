from pathlib import Path

import structlog

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(levelname)8s]: %(message)s',  # noqa: WPS323
        },
        'json_formatter': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.JSONRenderer(),
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
        },
        'json_file': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': Path.cwd() / 'logs' / 'django_structlog.log',
            'formatter': 'json_formatter',
        },
    },
    'loggers': {
        'django_structlog': {
            'handlers': ['console', 'json_file'],
            'level': 'INFO',
        },
    },
}
