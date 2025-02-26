import json
import logging
from pathlib import Path

import structlog
from django.core.exceptions import RequestDataTooBig
from django.dispatch import receiver
from django_structlog import signals

logging.basicConfig(filename=Path.cwd() / 'logs' / 'django_structlog.log')

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


@receiver(signals.bind_extra_request_metadata)
def bind_request_body(request, logger, **kwargs):
    try:
        request_body = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, RequestDataTooBig, UnicodeDecodeError):
        request_body = None

    structlog.contextvars.bind_contextvars(request_body=request_body)
