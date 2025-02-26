from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .address.views import CityViewSet
from .arketa.views import ArketaFeedbackViewSet, ArketaFileViewSet, ArketaTaskViewSet, ArketaTradePointViewSet
from .celery.views import CeleryResultView
from .departaments.views import DepartmentViewSet
from .document.views import InnViewSet, PassportViewSet, RegistrationViewSet, SelfieViewSet, SnilsViewSet
from .document.views.all_documents import DocumentViewSet
from .ext.views import HealthView
from .faq.views import FaqViewSet
from .file.views import FileViewSet, ImageViewSet
from .news.views.news import NewsViewSet
from .news.views.news_mailing import NewsMailingViewSet
from .projects.views import ProjectViewSet
from .promotion.views import PromotionMailingViewSet, PromotionViewSet
from .regions.views import RegionViewSet
from .settings.views import SettingsViewSet
from .stories.views.stories import StoriesViewSet
from .stories.views.stories_mailing import StoriesMailingViewSet
from .survey.views import SurveyMailingViewSet, SurveyViewSet
from .user.mobile.views import MobileViewSet
from .user.views import UserViewSet

router = routers.DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet, basename='devices')
router.register('settings', SettingsViewSet, basename='settings')
router.register('user', UserViewSet, basename='user')
router.register('user', MobileViewSet, basename='user_mobile')
router.register('file', FileViewSet, basename='file')
router.register('image', ImageViewSet, basename='image')
router.register('faq', FaqViewSet, basename='faq')
router.register('address/city', CityViewSet, basename='address')
router.register('document/inn', InnViewSet, basename='document_inn')
router.register('document/passport', PassportViewSet, basename='document_passport')
router.register('document/registration', RegistrationViewSet, basename='document_registration')
router.register('document/selfie', SelfieViewSet, basename='document_selfie')
router.register('document/snils', SnilsViewSet, basename='document_snils')
router.register('document', DocumentViewSet, basename='document_all')
router.register('news', NewsViewSet, basename='news')
router.register('news_mailing', NewsMailingViewSet, basename='news_mailing')
router.register('stories', StoriesViewSet, basename='stories')
router.register('stories_mailing', StoriesMailingViewSet, basename='stories_mailing')
router.register('promotions', PromotionViewSet, basename='promotions')
router.register('promotions_mailing', PromotionMailingViewSet, basename='promotions_mailing')
router.register('departments', DepartmentViewSet, basename='departments')
router.register('projects', ProjectViewSet, basename='projects')
router.register('regions', RegionViewSet, basename='regions')
router.register('arketa/task', ArketaTaskViewSet, basename='arketa_task')
router.register('arketa/trade_point', ArketaTradePointViewSet, basename='arketa_trade_point')
router.register('arketa/file', ArketaFileViewSet, basename='arketa_file')
router.register('arketa/feedback', ArketaFeedbackViewSet, basename='arketa_feedback')
router.register('surveys', SurveyViewSet, basename='surveys')
router.register('surveys_mailing', SurveyMailingViewSet, basename='surveys_mailing')


schema_view = get_schema_view(
    openapi.Info(
        title='RABOTUT API',
        default_version='v1',
        description='Routes of RABOTUT',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include((router.urls, 'api-root')), name='api-root'),
    path('celery/result/<pk>/', CeleryResultView.as_view()),
    path('health_check/', HealthView.as_view()),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
