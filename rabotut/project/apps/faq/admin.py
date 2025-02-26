from django.contrib import admin

from apps.faq.models import Faq


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'body')
