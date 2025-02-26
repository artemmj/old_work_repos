from rest_framework import permissions

from apps.organization.models import Membership, MembershipRoleChoices
from apps.user.models import RoleChoices


class IsSuperUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and RoleChoices.CUSTOMER in request.user.roles)


class IsInspector(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and RoleChoices.INSPECTOR in request.user.roles)


class IsDispatcher(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and RoleChoices.DISPATCHER in request.user.roles)


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and RoleChoices.ADMINISTRATOR in request.user.roles)


class IsOrganizationOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return Membership.objects.filter(
            user=request.user,
            organization=request.organization,
            role=MembershipRoleChoices.OWNER,
        ).exists()


class IsOrganizationManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return Membership.objects.filter(
            user=request.user,
            organization=request.organization,
            role=MembershipRoleChoices.MANAGER,
        ).exists()


class IsOrganizationInspector(permissions.BasePermission):
    def has_permission(self, request, view):
        return Membership.objects.filter(
            user=request.user,
            organization=request.organization,
            role=MembershipRoleChoices.INSPECTOR,
        ).exists()
