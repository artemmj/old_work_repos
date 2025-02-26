from channels.routing import ProtocolTypeRouter, URLRouter

from apps.websocket import routing
from apps.websocket.middleware import JWTAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddleware(
        URLRouter(
            routing.websockets_urlpatterns,
        ),
    ),
})
