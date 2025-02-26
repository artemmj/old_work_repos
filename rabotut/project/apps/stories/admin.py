from django.contrib import admin

from apps.stories.models import (
    Stories,
    StoriesMailingDepartment,
    StoriesMailingProject,
    StoriesMailingRegion,
    StoriesMailingUserRole,
    StoriesRead,
)


@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'background_color_button', 'text_color', 'created_at', 'deleted_at')
    filter_horizontal = ('slides',)
    search_fields = ('name',)


@admin.register(StoriesMailingDepartment)
class StoriesMailingDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'stories', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('stories', 'departments')


@admin.register(StoriesMailingProject)
class StoriesMailingProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'stories', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('stories', 'projects')


@admin.register(StoriesMailingRegion)
class StoriesMailingRegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'stories', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('stories', 'regions')


@admin.register(StoriesMailingUserRole)
class StoriesMailingUserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'stories', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('stories',)


@admin.register(StoriesRead)
class StoriesReadAdmin(admin.ModelAdmin):
    list_display = ('id', 'stories', 'user', 'created_at', 'updated_at')
    raw_id_fields = ('stories', 'user')
