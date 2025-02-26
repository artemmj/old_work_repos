from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from .celery.views import CeleryResultView
from .channel.views import ChannelViewSet
from .ext.views import HealthView
from .file.views import FileViewSet, ImageViewSet
from .message.views import MessageViewSet
from .settings.views import SettingsViewSet
from .user.views import UserViewSet

router = routers.DefaultRouter()
router.register('settings', SettingsViewSet, basename='settings')
router.register('user', UserViewSet, basename='user')
router.register('file', FileViewSet, basename='file')
router.register('image', ImageViewSet, basename='image')
router.register('posts', MessageViewSet, basename='posts')
router.register('channel', ChannelViewSet, basename='channel')

schema_view = get_schema_view(
    openapi.Info(title='Telegram Scraping API', default_version='v1', description='Routes of Telegram Scraping API'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger(<str:format>.json|.yaml)/', schema_view.without_ui(), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc'), name='schema-redoc'),
    path('', include((router.urls, 'api-root')), name='api-root'),
    path('celery/result/<pk>/', CeleryResultView.as_view()),
    path('health_check/', HealthView.as_view()),
]
