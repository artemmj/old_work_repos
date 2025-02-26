from django.contrib import admin

from apps.car.models.brand import Brand
from apps.car.models.car import Car
from apps.car.models.category import Category
from apps.car.models.generation import Generation
from apps.car.models.model import Model
from apps.car.models.modification import Modification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'brand')
    search_fields = ('title', 'brand__title', 'category__title')
    list_filter = ('category__title',)
    raw_id_fields = ('brand',)


@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'brand', 'model')
    search_fields = ('title', 'category__title', 'brand__title', 'model__title')
    list_filter = ('category__title',)
    raw_id_fields = ('brand', 'model')


@admin.register(Modification)
class ModificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'model', 'generation')
    search_fields = ('title', 'brand__title', 'model__title')
    list_filter = ('drive_type', 'engine_type', 'gearbox_type', 'generation__category__title')
    raw_id_fields = ('brand', 'model', 'generation')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'vin_code', 'gov_number', 'brand', 'model', 'generation')
    search_fields = ('vin_code', 'gov_number', 'brand__title', 'model__title')
    raw_id_fields = ('brand', 'model', 'generation', 'modification')
