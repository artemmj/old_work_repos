from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'email', 'username', 'role', 'first_name', 'last_name', 'doc_status', 'id')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role', 'is_self_employed', 'doc_status')}),
        (_('Personal info'), {'fields': ('first_name', 'middle_name', 'last_name', 'arketa_user_id')}),
        (_('Contact info'), {'fields': ('phone', 'email', 'city', 'department', 'regions', 'projects', 'location')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('phone',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'first_name',
                'last_name',
                'email',
                'phone',
                'role',
                'department',
                'regions',
                'projects',
                'password1',
                'password2',
            ),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')
