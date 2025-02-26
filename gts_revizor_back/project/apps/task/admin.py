from django.contrib import admin

from apps.product.models import ScannedProduct
from apps.task.models import Task


class ScannedProductInline(admin.StackedInline):
    model = ScannedProduct
    fields = ('id', 'created_at', 'product', 'amount', 'added_by_product_code')
    readonly_fields = ('id', 'created_at')
    extra = 0
    raw_id_fields = ('product',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'zone', 'type', 'employee', 'terminal', 'status', 'result', 'created_at')
    list_filter = ('zone__project',)
    inlines = [ScannedProductInline]
