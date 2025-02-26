import string

import structlog

from apps.helpers.services import AbstractService
from apps.user.models import User

log = structlog.get_logger(__name__)


class CreateUserService(AbstractService):
    def __init__(self):
        self.log = log.bind(action='create_user_service')

    def process(self, phone: str):
        password = User.objects.make_random_password(6, allowed_chars=string.digits)
        user, created = User.objects.get_or_create(phone=phone)
        if created:
            user.set_password(password)
            user.save()
            self.log.info('Пользователь создан', phone=user.phone)
