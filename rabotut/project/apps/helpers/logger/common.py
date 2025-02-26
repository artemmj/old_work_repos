import uuid

import structlog

from .consts import REQUEST_HEADER_KEY


def get_request_id() -> str:
    """Возвращает request_id из контекста выполнения."""
    return structlog.contextvars.get_contextvars().get(REQUEST_HEADER_KEY) or str(uuid.uuid4())
