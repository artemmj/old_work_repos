from django.contrib import admin

from apps.tariffs.models import Subscription, Tariff


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'period', 'amount')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tariff', 'organization', 'amount', 'is_active', 'auto_renewal')
