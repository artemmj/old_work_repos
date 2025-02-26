from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.user.models import ConfirmationCode

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'middle_name',
            'agreement_processing',
            'agreement_policy',
            'roles',
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name',
                'middle_name',
                'email',
                'phone',
                'password1',
                'password2',
                'roles',
            ),
        }),
    )

    list_display = (
        'id',
        'last_name',
        'first_name',
        'middle_name',
        'email',
        'phone',
        'agreement_processing',
        'agreement_policy',
        'roles',
    )
    search_fields = ('phone', 'first_name', 'last_name')
    ordering = ('-created_at',)


@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code')
    search_fields = ('phone', )
