from django.contrib import admin

from apps.file.models import File
from apps.message.models import Message


class FileInline(admin.StackedInline):
    model = File
    extra = 0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'channel', 'text')
    list_filter = ('channel',)
    inlines = (FileInline,)
