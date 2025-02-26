from django.contrib import admin

from apps.channel.models import Channel


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('link', 'is_active', 'created_at', 'id')
