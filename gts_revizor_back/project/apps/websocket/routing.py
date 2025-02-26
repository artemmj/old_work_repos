from django.conf.urls import url

from apps.websocket.consumers import WebsocketConsumer

websockets_urlpatterns = [
    url(r'^ws/', WebsocketConsumer.as_asgi()),  # noqa: WPS360
]
