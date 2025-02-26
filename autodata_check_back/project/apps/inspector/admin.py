from django.contrib import admin

from apps.inspector.models import Inspector, Requisite


@admin.register(Inspector)
class InspectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'inn')
    search_fields = ('inn', 'user__first_name', 'user__last_name')
    readonly_fields = ('balance',)


@admin.register(Requisite)
class RequisiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'inspector', 'inn')
