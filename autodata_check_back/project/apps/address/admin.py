from django.contrib import admin

from apps.address.models import Address, City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('fias_id', 'title', 'inspection_price')
    search_fields = ('title',)
    fieldsets = (
        (None, {'fields': ('fias_id', 'title', 'latitude', 'longitude', 'inspection_price')}),
    )
    readonly_fields = ('fias_id', 'title', 'latitude', 'longitude')

    def has_add_permission(self, request):
        return False


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'title')
    search_fields = ('title',)
    fieldsets = (
        (None, {'fields': ('city', 'title', 'latitude', 'longitude')}),
    )

    def has_change_permission(self, request, obj=None):   # noqa: WPS110
        return False

    def has_add_permission(self, request):
        return False
