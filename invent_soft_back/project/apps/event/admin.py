from django.contrib import admin

from apps.event.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'fake_id', 'created_at', 'title', 'project', 'comment')
    list_filter = ('project',)
    search_fields = ('title',)
    ordering = ['-created_at']
    fields = ('id', 'created_at', 'project', 'title', 'comment')
    readonly_fields = ('id', 'created_at')
