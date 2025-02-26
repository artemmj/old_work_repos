from django.contrib import admin

from .models import (
    Promotion,
    PromotionEmoji,
    PromotionMailingDepartment,
    PromotionMailingProject,
    PromotionMailingRegion,
    PromotionMailingUserRole,
    PromotionRead,
)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'end_date', 'is_top', 'is_main_display', 'is_hidden')
    search_fields = ('name',)


@admin.register(PromotionMailingDepartment)
class PromotionMailingDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'publish_datetime', 'promotion', 'is_published', 'is_push')


@admin.register(PromotionMailingProject)
class PromotionMailingProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'publish_datetime', 'promotion', 'is_published', 'is_push')


@admin.register(PromotionMailingRegion)
class PromotionMailingRegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'publish_datetime', 'promotion', 'is_published', 'is_push')


@admin.register(PromotionMailingUserRole)
class PromotionMailingUserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'publish_datetime', 'promotion', 'is_published', 'is_push')


@admin.register(PromotionEmoji)
class PromotionEmojiAdmin(admin.ModelAdmin):
    list_display = ('id', 'promotion', 'user', 'emoji_type')


@admin.register(PromotionRead)
class PromotionReadAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'promotion', 'user')
