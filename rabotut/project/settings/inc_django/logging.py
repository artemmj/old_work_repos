import logging
import os

import orjson
import structlog


def add_environment(_, __, event_dict):
    """Добавляет окружение в логи."""
    event_dict['build'] = os.getenv('BUILD')
    return event_dict


pre_chain = [
    structlog.processors.TimeStamper(fmt='iso', utc=True),
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    add_environment,
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': 'INFO', 'handlers': []},
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(levelname)8s]: %(message)s',  # noqa: WPS323
        },
        'json_formatter': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.JSONRenderer(),
            'foreign_pre_chain': pre_chain,
        },
    },
    'handlers': {
        'default_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
        },
        'structlog_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json_formatter',
        },
    },
    'loggers': {
        'django_default': {
            'handlers': ['default_console'],
            'level': 'INFO',
        },
        'django_structlog': {
            'handlers': ['structlog_console'],
            'level': 'INFO',
        },
    },
}

structlog.configure(
    cache_logger_on_first_use=True,
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        add_environment,
        structlog.processors.format_exc_info,
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            },
        ),
        structlog.processors.TimeStamper(fmt='iso', utc=True),
        structlog.processors.JSONRenderer(serializer=orjson.dumps),
    ],
    logger_factory=structlog.BytesLoggerFactory(),
)
