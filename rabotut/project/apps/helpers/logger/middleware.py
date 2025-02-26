import uuid
from typing import Optional

import sentry_sdk
import structlog
from django.conf import settings
from django.http import HttpRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError

log = structlog.get_logger()


def get_user_by_token(request: HttpRequest) -> Optional[str]:  # noqa: WPS212
    """Получение id пользователя из валидного токена."""
    try:
        user_id_claim = settings.SIMPLE_JWT['USER_ID_CLAIM']
    except KeyError:
        return None

    jwt_authentication = JWTAuthentication()
    header = jwt_authentication.get_header(request)
    if header is None:
        return None

    try:
        raw_token = jwt_authentication.get_raw_token(header)
    except AuthenticationFailed:
        return None

    if raw_token is None:
        return None

    try:
        validated_token = jwt_authentication.get_validated_token(raw_token)
    except (TokenError, InvalidToken):
        return None

    try:
        user_id = validated_token[user_id_claim]
    except KeyError:
        return None

    return user_id


class ContextLogMiddleware:
    """Сохранение контекста для записи лога."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.META.get('HTTP_X_REQUEST_ID')
        user_id = get_user_by_token(request)

        if not request_id:
            request_id = str(uuid.uuid4())

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            api=request.get_full_path_info(),
            request_id=request_id,
            user_id=user_id,
            platform=request.META.get('HTTP_PLATFORM'),
            app_version=request.META.get('HTTP_APP_VERSION'),
            user_agent=request.META.get('HTTP_USER_AGENT'),
        )
        # see https://blog.sentry.io/2019/01/31/using-nginx-sentry-trace-errors-logs/
        if request_id:
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag('request_id', request_id)

        log.info(
            'Запрос к апи',
            device_id=request.META.get('HTTP_DEVICE_ID'),
            device_name=request.META.get('HTTP_DEVICE_NAME'),
            os_version=request.META.get('HTTP_OS_VERSION'),
            # дебаг сборка - например есть возможности обхода бизнес логики (подмена локаций и тд)
            debuggable=request.META.get('HTTP_DEBUGGABLE'),
        )
        return self.get_response(request)
