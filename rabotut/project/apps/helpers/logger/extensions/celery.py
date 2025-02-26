import uuid
from typing import TYPE_CHECKING, Any, Dict

import sentry_sdk
import structlog

from ..consts import REQUEST_HEADER_KEY


def celery_log_extension() -> None:
    """Перенос request_id из HTTP запроса в Celery worker."""
    try:  # noqa: WPS229
        import celery  # noqa: F401, WPS433
        from celery.signals import before_task_publish, task_postrun, task_prerun  # noqa: WPS433

        if TYPE_CHECKING:
            from celery import Task  # noqa: WPS458
    except ImportError:
        return

    @before_task_publish.connect(weak=False)
    def transfer_request_id(headers: Dict[str, str], **kwargs: Any) -> None:  # noqa: WPS430
        """Перенос request_id из контекста потока основного приложения в Celery worker."""
        request_id = structlog.contextvars.get_contextvars().get(REQUEST_HEADER_KEY)

        if request_id:
            headers[REQUEST_HEADER_KEY] = request_id

    @task_prerun.connect(weak=False)
    def load_request_id(task: 'Task', **kwargs: Any) -> None:  # noqa: WPS430
        """Устанавливает request_id из заголовка в контекст для записи логов.

        Или генерирует новый на основе correlation_id если request_id отсутствует.
        """
        request_id = task.request.get(REQUEST_HEADER_KEY)
        if request_id is None:
            request_id = uuid.uuid4().hex

        structlog.contextvars.bind_contextvars(request_id=request_id)
        # see https://blog.sentry.io/2019/01/31/using-nginx-sentry-trace-errors-logs/
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag('request_id', request_id)

    @task_postrun.connect(weak=False)
    def cleanup(**kwargs: Any) -> None:  # noqa: WPS430
        """Очистка контекста."""
        structlog.contextvars.clear_contextvars()
