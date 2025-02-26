from django.db import models


class UserRolesChoices(models.TextChoices):
    APPLICANT = 'applicant', 'Аппликант'
    EMPLOYEE = 'employee', 'Сотрудник'
    SUPERVISOR = 'supervisor', 'Супервизор'
    CANDIDATE = 'candidate', 'Кандидат'
    DISMISSED = 'dismissed', 'Уволенный'
    APPLICANT_CONFIRMED = 'applicant_confirmed', 'Аппликант подтвержденный'
