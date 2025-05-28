from rest_framework import permissions


class IsSuperadminAndAdminOnly(permissions.BasePermission):
    """
    Custom permission to only allow super admins to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a super admin
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)
    