from django.db import models


class UserDocStatuses(models.TextChoices):
    APPROVAL = 'approval', 'Проверка'
    ACCEPT = 'accept', 'Подтвержден'
    DECLINE = 'decline', 'Отклонен'
