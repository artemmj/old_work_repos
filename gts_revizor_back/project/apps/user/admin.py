from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from fcm_django.models import FCMDevice

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'middle_name', 'last_name', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (User.USERNAME_FIELD, 'password1', 'password2'),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')
    list_display = ('phone', 'email', 'username', 'is_staff', 'first_name', 'middle_name', 'last_name')


admin.site.unregister(Group)
admin.site.unregister(FCMDevice)
