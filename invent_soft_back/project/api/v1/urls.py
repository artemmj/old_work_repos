from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .celery.views import CeleryResultView
from .changelog.views import ChangeLogViewSet
from .document.views import DocumentViewSet
from .employee.views import EmployeeViewSet
from .event.views import EventViewSet
from .ext.views import HealthView
from .file.views import FileViewSet
from .product.views import ProductViewSet, ScannedProductViewSet
from .project.views import ProjectViewSet
from .project.views.rmm_settings import RMMSettingsViewSet
from .project.views.terminal_settings import TerminalSettingsViewSet
from .reports.views import ReportsViewSet
from .settings.views import SettingsViewSet
from .sync.views import SyncViewSet
from .task.views import TaskViewSet
from .template.views import TemplateExportViewSet, TemplateViewSet
from .terminal.views import TerminalViewSet
from .user.views import UserViewSet
from .zone.views import ZoneViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('project', ProjectViewSet, basename='project')
router.register('rmm_settings', RMMSettingsViewSet, basename='rmm_settings')
router.register('terminal_settings', TerminalSettingsViewSet, basename='terminal_settings')
router.register('file', FileViewSet, basename='file')
router.register('template', TemplateViewSet, basename='template')
router.register('template_export', TemplateExportViewSet, basename='template_export')
router.register('employee', EmployeeViewSet, basename='employee')
router.register('zone', ZoneViewSet, basename='zone')
router.register('product', ProductViewSet, basename='product')
router.register('scanned_product', ScannedProductViewSet, basename='scanned_product')
router.register('terminal', TerminalViewSet, basename='terminal')
router.register('task', TaskViewSet, basename='task')
router.register('event', EventViewSet, basename='event')
router.register('document', DocumentViewSet, basename='document')
router.register('reports', ReportsViewSet, basename='reports')
router.register('sync', SyncViewSet, basename='sync')
router.register('change-log', ChangeLogViewSet, basename='change-log')
router.register('settings', SettingsViewSet, basename='settings')

schema_view = get_schema_view(
    openapi.Info(title='GTS REVIZOR API', default_version='v1', description='Routes of GTS REVIZOR project'),
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
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
