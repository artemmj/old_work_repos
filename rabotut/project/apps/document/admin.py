from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from apps.document.models import Inn, Passport, Registration, Selfie, SelfieRecognition, Snils


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'number', 'series', 'status')
    list_filter = ('status',)
    raw_id_fields = ('user',)
    history_list_display = list_display
    date_hierarchy = 'created_at'


@admin.register(Inn)
class InnAdmin(admin.ModelAdmin):
    list_display = ('value', 'user', 'status', 'is_self_employed', 'verification_at')
    list_filter = ('status',)
    raw_id_fields = ('user',)
    history_list_display = list_display
    date_hierarchy = 'created_at'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_address', 'status')
    list_filter = ('status',)
    raw_id_fields = ('user',)
    history_list_display = list_display
    date_hierarchy = 'created_at'


@admin.register(Snils)
class SnilsAdmin(admin.ModelAdmin):
    list_display = ('user', 'value', 'status')
    list_filter = ('status',)
    raw_id_fields = ('user',)
    history_list_display = list_display
    date_hierarchy = 'created_at'


class SelfieRecognitionInline(admin.StackedInline):
    model = SelfieRecognition
    extra = 0


@admin.register(Selfie)
class SelfieAdmin(SimpleHistoryAdmin):
    inlines = [SelfieRecognitionInline]
    list_display = ('user', 'status')
    list_filter = ('status',)
    raw_id_fields = ('user',)
    history_list_display = list_display
    date_hierarchy = 'created_at'
