from django.contrib import admin

from apps.product.models import AdditionalProductTitleAttribute, FileOfProjectProducts, Product, ScannedProduct


class AdditionalProductTitleAttributeInlineAdmin(admin.StackedInline):
    extra = 0
    model = AdditionalProductTitleAttribute


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'vendor_code', 'barcode', 'title', 'price', 'remainder', 'dm')
    search_fields = ('title', 'barcode')
    list_filter = ('project',)
    inlines = (AdditionalProductTitleAttributeInlineAdmin, )


@admin.register(ScannedProduct)
class ScannedProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'get_product_barcode',
        'get_product_document',
        'amount',
        'scanned_time',
        'added_by_product_code',
    )
    list_filter = ('task__zone__project',)
    raw_id_fields = ('product', 'task')
    search_fields = ('product__barcode', 'task__counter_scan_document__id')

    def get_product_barcode(self, scanned_product):
        return scanned_product.product.barcode
    get_product_barcode.short_description = 'Штрих-код товара'

    def get_product_document(self, scanned_product: ScannedProduct):
        return scanned_product.task.counter_scan_document.first()
    get_product_document.short_description = 'Документ'


@admin.register(FileOfProjectProducts)
class FileOfProjectProductsAdmin(admin.ModelAdmin):
    list_display = ('project', 'products_file')


@admin.register(AdditionalProductTitleAttribute)
class AdditionalProductTitleAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'content', 'is_hidden', 'project')
    list_filter = ('project', 'is_hidden')
    search_fields = ('id', 'product__title', 'product__id')
