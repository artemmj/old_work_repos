from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework import permissions, routers

from api.v1.car.views.car import CarViewSet
from api.v1.inspection.views.client import ClientViewSet
from api.v1.inspection.views.completeness import CompletenessViewSet
from api.v1.inspection.views.damage import DamageViewSet
from api.v1.inspection.views.documents import DocumentViewSet
from api.v1.inspection.views.equipment import EquipmentViewSet
from api.v1.inspection.views.inspection import InspectionViewSet
from api.v1.inspection.views.lift import LiftViewSet
from api.v1.inspection.views.paintwork import PaintWorkViewSet
from api.v1.inspection.views.photos import PhotosViewSet
from api.v1.inspection.views.technical import TechnicalViewSet
from api.v1.inspection.views.tires import TiresViewSet
from api.v1.user.views.common import UserViewSet

from .address.views import AddressViewSet
from .car.views.brand import BrandViewSet
from .car.views.category import CategoryViewSet
from .car.views.generation import GenerationViewSet
from .car.views.model import ModelViewSet
from .car.views.modification import ModificationViewSet
from .celery.views import CeleryResultView
from .city.views import CityViewSet
from .ext.views import HealthView
from .file.views import DBFileViewSet, FileViewSet, ImageViewSet
from .inspection.views.sign_client import SignClientViewSet
from .inspection.views.sign_inspector import SignInspectorViewSet
from .inspection.views.video import VideoViewSet
from .inspection_task.views.invitation import InvitationViewSet
from .inspection_task.views.task import InspectionTaskViewSet
from .inspector_accreditation.views import AccreditationInspectionViewSet, InspectorAccreditationRequestViewSet
from .notification.views import NotificationViewSet
from .organization.views import OrganizationViewSet
from .organization.views.invitation import OrgInvitationViewSet
from .organization.views.membership import MembershipViewSet
from .settings.views import SettingsViewSet
from .tariffs.views import TariffViewSet
from .template.views import TemplateViewSet
from .template.views.invitation import TemplateInvitationViewSet
from .transaction.views.inspector import InspectorTransactionViewSet
from .transaction.views.organization import OrganizationTransactionViewSet

router = routers.DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet, basename='devices')
router.register('settings', SettingsViewSet, basename='settings')
router.register('user', UserViewSet, basename='user')
router.register('file', FileViewSet, basename='file')
router.register('image', ImageViewSet, basename='image')
router.register('car', CarViewSet, basename='car')
router.register('category', CategoryViewSet, basename='category')
router.register('brand', BrandViewSet, basename='brand')
router.register('model', ModelViewSet, basename='model')
router.register('generation', GenerationViewSet, basename='generation')
router.register('modification', ModificationViewSet, basename='modification')
router.register('db_file', DBFileViewSet, basename='db_file')
router.register('client', ClientViewSet, basename='client')
router.register('completeness', CompletenessViewSet, basename='completeness')
router.register('photos', PhotosViewSet, basename='photos')
router.register('video', VideoViewSet, basename='video')
router.register('equipment', EquipmentViewSet, basename='equipment')
router.register('documents', DocumentViewSet, basename='documents')
router.register('tires', TiresViewSet, basename='tires')
router.register('technical', TechnicalViewSet, basename='technical')
router.register('lift', LiftViewSet, basename='lift')
router.register('paintwork', PaintWorkViewSet, basename='paintwork')
router.register('damage', DamageViewSet, basename='damage')
router.register('inspection', InspectionViewSet, basename='inspection')
router.register('inspection_task', InspectionTaskViewSet, basename='inspection_task')
router.register('invitation', InvitationViewSet, 'invitation')
router.register('transaction/organization', OrganizationTransactionViewSet, basename='transaction_organization')
router.register('transaction/inspector', InspectorTransactionViewSet, basename='transaction_inspector')
router.register('address', AddressViewSet, basename='address')
router.register('city', CityViewSet, basename='city')
router.register('organization', OrganizationViewSet, basename='organization')
router.register('memberships', MembershipViewSet, basename='memberships')
router.register('org_invitation', OrgInvitationViewSet, basename='org_invitation')
router.register('template', TemplateViewSet, basename='template')
router.register('template_invitation', TemplateInvitationViewSet, basename='template_invitation')
router.register('accreditation_request', InspectorAccreditationRequestViewSet, basename='accreditation_request')
router.register('accreditation_inspection', AccreditationInspectionViewSet, basename='accreditation_inspection')
router.register('sign_client', SignClientViewSet, basename='sign_client')
router.register('sign_inspector', SignInspectorViewSet, basename='sign_inspector')
router.register('tariffs', TariffViewSet, basename='tariffs')
router.register('notification', NotificationViewSet, basename='notification')

schema_view = get_schema_view(
    openapi.Info(title='AutoInspector API', default_version='v1', description='Routes of AutoInspector project'),
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
