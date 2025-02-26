from django.contrib import admin

from apps.organization.models import Membership, Organization, OrgInvitation, PreparatoryInvitation


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0
    raw_id_fields = ('user',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'legal_title', 'inn', 'balance')
    search_fields = ('title', 'legal_title', 'inn')
    readonly_fields = ('balance', 'owner')
    inlines = [MembershipInline]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'organization', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'organization__title', 'organization__legal_title')
    list_filter = ('organization',)


@admin.register(OrgInvitation)
class OrgInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'organization', 'role', 'is_accepted')
    search_fields = ('phone',)
    list_filter = ('role', 'is_accepted')


@admin.register(PreparatoryInvitation)
class PreparatoryInvitationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'organization', 'is_active')
    search_fields = ('phone',)
    list_filter = ('organization',)
