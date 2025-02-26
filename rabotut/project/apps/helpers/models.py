import uuid
from typing import Type

from django.contrib.postgres.fields import ArrayField
from django.core import exceptions
from django.db import connection, models
from django.forms import SelectMultiple, TypedMultipleChoiceField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import DeletedManager, UserDeletedManager


def get_next_value(name):
    with connection.cursor() as cursor:
        cursor.execute(f"select nextval('{name}');")
        row = cursor.fetchone()
    return row[0]


def get_or_repair_or_create(model, *args, **kwargs):
    obj, _ = model.objects.get_or_create(*args, **kwargs)  # noqa: WPS110
    if obj.deleted_at:
        obj.deleted_at = None
        obj.save()
    return obj


def get_or_repair_or_update(model, *args, **kwargs):
    obj, _ = model.objects.update_or_create(*args, **kwargs)  # noqa: WPS110
    if obj.deleted_at:
        obj.deleted_at = None
        obj.save()
    return obj


class ForceCleanModel(models.Model):
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(_('ID'), default=uuid.uuid4, primary_key=True, editable=False)  # noqa: WPS221

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        abstract = True


class DeletedModel(models.Model):
    deleted_at = models.DateTimeField(
        _('deleted at'),
        db_index=True,
        null=True,
        blank=True,
        editable=False,
    )

    objects = DeletedManager()  # noqa: WPS110

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()  # noqa: WPS601
            self.save()


class UserDeletedModel(models.Model):
    deleted_at = models.DateTimeField(
        _('deleted at'),
        db_index=True,
        null=True,
        blank=True,
        editable=False,
    )

    objects = UserDeletedManager()  # noqa: WPS110

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()  # noqa: WPS601
            self.save()


class FilterTypes(models.TextChoices):
    GENERAL = 'general', 'общая'
    ACTUAL = 'actual', 'актуальная'


def enum_max_length(text_choices: Type[models.Choices]) -> int:
    return max(len(value) for value in text_choices.values)  # noqa: WPS110


class DefaultModel(models.Model):
    """Стандартный базовый класс для django моделей.

    Объединяет в себе функциональность UUIDModel, CreatedModel, UpdatedModel, DeletedModel.
    """

    id = models.UUIDField(_('ID'), default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлен'), auto_now=True)
    deleted_at = models.DateTimeField(_('Удален'), db_index=True, null=True, blank=True, editable=False)

    objects = DeletedManager()  # noqa: WPS110

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            self.deleted_at = timezone.now()  # noqa: WPS601
            self.save()


class ArraySelectMultiple(SelectMultiple):

    def value_omitted_from_data(self, data, files, name):
        return False


class ChoiceArrayField(ArrayField):
    """
    A postgres ArrayField that supports the choices property.

    Ref. https://gist.github.com/danni/f55c4ce19598b2b345ef.
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': TypedMultipleChoiceField,
            'choices': self.base_field.choices,
            'coerce': self.base_field.to_python,
            'widget': ArraySelectMultiple,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)

    def to_python(self, value):
        res = super().to_python(value)
        if isinstance(res, list):
            value = [self.base_field.to_python(val) for val in res]
        return value

    def validate(self, value, model_instance):
        if not self.editable:
            # Skip validation for non-editable fields.
            return

        if self.choices is not None and value not in self.empty_values:
            if set(value).issubset({option_key for option_key, _ in self.choices}):
                return
            raise exceptions.ValidationError(
                self.error_messages['invalid_choice'],
                code='invalid_choice',
                params={'value': value},
            )

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'], code='null')

        if not self.blank and value in self.empty_values:
            raise exceptions.ValidationError(self.error_messages['blank'], code='blank')
