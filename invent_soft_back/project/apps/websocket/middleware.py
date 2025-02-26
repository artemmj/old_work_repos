import logging
import traceback

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from jwt import decode as jwt_decode

User = get_user_model()
logger = logging.getLogger('django')


class JWTAuthMiddleware:
    """Middleware for Django Channels 2."""

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):  # noqa: WPS231
        """Middleware для jwt аутентификации."""
        headers = {item[0].decode('utf8'): item[1].decode('utf8') for item in scope['headers']}
        query_string = scope['query_string'].decode('utf8').split('=')
        close_old_connections()

        try:  # noqa: WPS229
            jwt_token = None
            if headers.get('jwt-token'):
                jwt_token = headers.get('jwt-token')
            elif len(query_string) == 2 and query_string[0] == 'token':
                jwt_token = query_string[1]

            if jwt_token:
                jwt_payload = self.get_payload(jwt_token)
                user_id = self.get_user_id(jwt_payload)
                scope['user_id'] = user_id
            else:
                scope['user_id'] = None
        except (InvalidSignatureError, KeyError, ExpiredSignatureError, DecodeError):
            traceback.print_exc()
        except BaseException:  # noqa: WPS424
            scope['user'] = None

        return await self.app(scope, receive, send)

    def get_payload(self, jwt_token):
        return jwt_decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])

    def get_user_id(self, payload):
        return payload['user_id']
