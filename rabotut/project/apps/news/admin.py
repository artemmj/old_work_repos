from django.contrib import admin

from apps.news.models import (
    News,
    NewsEmoji,
    NewsMailingDepartment,
    NewsMailingProject,
    NewsMailingRegion,
    NewsMailingUserRole,
    NewsRead,
)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'is_top', 'is_main_page', 'deleted_at')
    filter_horizontal = ('attachments',)
    search_fields = ('name',)


@admin.register(NewsMailingDepartment)
class NewsMailingDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('news', 'departments')


@admin.register(NewsMailingProject)
class NewsMailingProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('news', 'projects')


@admin.register(NewsMailingRegion)
class NewsMailingRegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('news', 'regions')


@admin.register(NewsMailingUserRole)
class NewsMailingUserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('news',)


@admin.register(NewsEmoji)
class NewsEmojiAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'user', 'emoji_type')
    raw_id_fields = ('news', 'user')


@admin.register(NewsRead)
class NewsReadAdmin(admin.ModelAdmin):
    list_display = ('id', 'news', 'user')
    raw_id_fields = ('news', 'user')
