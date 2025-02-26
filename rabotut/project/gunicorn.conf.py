import structlog

from apps.helpers.logger.processors import add_environment, gunicorn_log_parser

pre_chain = [
    structlog.processors.TimeStamper(fmt='iso', utc=True),
    structlog.stdlib.add_log_level,
    add_environment,
    gunicorn_log_parser,
]

logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': 'INFO', 'handlers': []},
    'formatters': {
        'json_formatter': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.JSONRenderer(),
            'foreign_pre_chain': pre_chain,
        },
    },
    'handlers': {
        'error_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json_formatter',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json_formatter',
        },
    },
}
