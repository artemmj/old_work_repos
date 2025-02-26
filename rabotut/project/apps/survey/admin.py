from django.contrib import admin

from .models import (
    Answer,
    Option,
    Question,
    Survey,
    SurveyMailingDepartments,
    SurveyMailingProjects,
    SurveyMailingRegions,
    SurveyMailingRoles,
)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_self_option')
    inlines = (QuestionInline,)


class OptionInline(admin.StackedInline):
    model = Option
    extra = 0


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'name', 'survey')
    list_filter = ('survey',)
    inlines = (OptionInline, AnswerInline)
    raw_id_fields = ('survey',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'name', 'question')
    list_filter = ('question',)
    raw_id_fields = ('question',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'self_option_answer')
    raw_id_fields = ('options',)


@admin.register(SurveyMailingDepartments)
class SurveyMailingDepartmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('departments',)


@admin.register(SurveyMailingProjects)
class SurveyMailingProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('projects',)


@admin.register(SurveyMailingRegions)
class SurveyMailingRegionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push')
    raw_id_fields = ('regions',)


@admin.register(SurveyMailingRoles)
class SurveyMailingRolesAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'publish_datetime', 'is_published', 'is_push')
