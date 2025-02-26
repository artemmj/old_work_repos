from rest_framework.permissions import BasePermission

from apps.user.models import UserRoles


class IsMasterPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.role == UserRoles.MASTER
        )


class IsApplicantPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.role == UserRoles.APPLICANT
        )


class IsApplicantConfirmedPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.role == UserRoles.APPLICANT_CONFIRMED
        )
