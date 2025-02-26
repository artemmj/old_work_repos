from django.contrib import admin

from apps.product.models import AdditionalProductTitleAttribute, FileOfProjectProducts, Product, ScannedProduct


class AdditionalProductTitleAttributeInlineAdmin(admin.StackedInline):
    extra = 0
    model = AdditionalProductTitleAttribute


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'project',
        'vendor_code',
        'barcode',
        'title',
        'price',
        'remainder',
        'dm',
        'size',
        'remainder_2',
        'qr_code',
    )
    search_fields = ('title', 'barcode')
    list_filter = ('project',)
    inlines = (AdditionalProductTitleAttributeInlineAdmin,)


@admin.register(ScannedProduct)
class ScannedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'task', 'amount', 'scanned_time', 'added_by_product_code', 'added_by_qr_code')
    list_filter = ('task__zone__project',)
    raw_id_fields = ('product',)


@admin.register(FileOfProjectProducts)
class FileOfProjectProductsAdmin(admin.ModelAdmin):
    list_display = ('project', 'products_file')


@admin.register(AdditionalProductTitleAttribute)
class AdditionalProductTitleAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'content', 'is_hidden', 'project')
    list_filter = ('project', 'is_hidden')
    search_fields = ('id', 'product__title', 'product__id')
