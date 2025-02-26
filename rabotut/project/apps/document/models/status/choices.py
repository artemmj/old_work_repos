from django.db import models


class BaseUserDocumentStatuses(models.TextChoices):
    APPROVAL = 'approval', 'Проверка'
    ACCEPT = 'accept', 'Подтвержден'
    DECLINE = 'decline', 'Отклонен'
