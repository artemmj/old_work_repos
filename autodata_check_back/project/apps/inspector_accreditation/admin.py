from django.contrib import admin

from apps.inspector_accreditation.models import AccreditationInspection, InspectorAccreditationRequest


@admin.register(InspectorAccreditationRequest)
class InspectorAccreditationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'user', 'inn', 'company', 'city')


@admin.register(AccreditationInspection)
class AccreditationInspectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status', 'template')
