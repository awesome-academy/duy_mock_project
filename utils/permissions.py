from rest_framework import permissions

from users.models import User


class IsActiveUser(permissions.BasePermission):
    """
    Custom permission to only allow active users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.status == User.UserStatus.ACTIVED
