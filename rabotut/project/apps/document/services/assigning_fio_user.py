from django.contrib.auth import get_user_model

from apps.document.models import Passport
from apps.helpers.services import AbstractService

User = get_user_model()


class AssigningFioUserService(AbstractService):
    """Сервис присваивает ФИО юзеру."""

    def __init__(self, passport: Passport, user: User):
        self.passport = passport
        self.user = user

    def process(self, *args, **kwargs):
        self.user.first_name = self.passport.first_name
        self.user.last_name = self.passport.last_name
        self.user.middle_name = self.passport.patronymic
        self.user.save()
