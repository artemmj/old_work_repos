from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from fcm_django.models import DeviceType, FCMDevice
from jwt import ExpiredSignatureError, InvalidSignatureError
from jwt import decode as jwt_decode
from jwt import get_unverified_header as jwt_get_unverified_header

User = get_user_model()


class DeviceMiddleware(MiddlewareMixin):
    device_name_header = 'HTTP_DEVICE_NAME'
    device_type_header = 'HTTP_DEVICE_TYPE'
    registration_id_header = 'HTTP_REGISTRATION_ID'
    token = 'HTTP_AUTHORIZATION'  # noqa: S105

    def process_request(self, request):  # noqa: WPS210, WPS231
        request.device = None
        user_id = None
        device_name = request.META.get(self.device_name_header, None)
        device_type = request.META.get(self.device_type_header, None)
        if device_type not in DeviceType.values:
            device_type = None
        registration_id = request.META.get(self.registration_id_header, None)
        token = request.META.get(self.token, None)
        if token:
            try:  # noqa: WPS229
                token = token.split(' ')[-1]
                algorithm = jwt_get_unverified_header(token).get('alg')
                payload = jwt_decode(jwt=token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=[algorithm])
                if payload['token_type'] == 'access':
                    user_id = payload['user_id']
            except (ExpiredSignatureError, InvalidSignatureError, KeyError):
                pass

        if registration_id and device_type and user_id and User.objects.filter(id=user_id).exists():
            request.device, _ = FCMDevice.objects.update_or_create(  # noqa: WPS414
                registration_id=registration_id,
                type=device_type,
                defaults={
                    'user_id': user_id,
                    'name': device_name,
                    'active': True,
                },
            )
        else:
            request.device = None
