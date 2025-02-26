from django.db import models


class UserRolesChoices(models.TextChoices):
    APPLICANT = 'applicant', 'Аппликант'
    EMPLOYEE = 'employee', 'Сотрудник'
    SUPERVISOR = 'supervisor', 'Супервизор'
    CANDIDATE = 'candidate', 'Кандидат'
    DISMISSED = 'dismissed', 'Уволенный'
    APPLICANT_CONFIRMED = 'applicant_confirmed', 'Аппликант подтвержденный'


class EmojiChoices(models.TextChoices):
    SMIRK = 'smirk', 'Ухмылка'
    THUMB_UP = 'thumb_up', 'Палец вверх'
    THUMB_DOWN = 'thumb_down', 'Палец вниз'
    FIRE = 'fire', 'Огонь'
    HEART = 'heart', 'Сердце'
    SHOCK = 'shock', 'Удивление'
