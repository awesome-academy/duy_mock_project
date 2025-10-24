from rest_framework import permissions
from working_space_managers.models import WorkingSpaceManager


class IsWorkingSpaceManager(permissions.BasePermission):
    """
    Custom permission to only allow working space managers to access the view.
    """

    def has_object_permission(self, request, view, obj):
        return WorkingSpaceManager.objects.filter(
            working_space=obj, user=request.user, role=WorkingSpaceManager.Role.ADMIN
        ).exists()
