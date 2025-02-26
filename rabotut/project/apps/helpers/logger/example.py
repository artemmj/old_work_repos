# 1 добавить настройки логов в настройки django и gunicorn (see gunicorn.conf.py)
# 2 подключить middleware ContextLogMiddleware

# Пример использования
import structlog

log = structlog.get_logger()


def some_function():
    # ...
    log.error("user did something", something="shot_in_foot")
    # ...


# Пример логов:
# django:
# {
#   "event":"health check!",
#   "request_id":"fd10fdfa659c5aa9fcce87ef4e639d06",
#   "user_id":"eb0f3f33-ddf9-4b87-9be6-b6b800507361",
#   "level":"info",
#   "stage":"dev",
#   "service":"ark_uber",
#   "build":"0d554ffc",
#   "pathname":"/app/api/v1/ext/views.py",
#   "lineno":10,
#   "func_name":"get",
#   "timestamp":"2022-09-19T15:29:24.446650Z"
# }
#
# gunicorn:
# {
#   "event": "fd10fdfa659c5aa9fcce87ef4e639d06 \"GET /api/v1/health_check/ HTTP/1.0\" 200 \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.5.1019 Yowser/2.5 Safari/537.36\"",
#   "timestamp": "2022-09-19T15:29:24.450777Z",
#   "level": "info",
#   "logger": "gunicorn.access",
#   "stage": "dev",
#   "service": "ark_uber",
#   "build": "0d554ffc",
#   "request_id": "fd10fdfa659c5aa9fcce87ef4e639d06"
# }
