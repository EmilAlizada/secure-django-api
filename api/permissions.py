from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Defense-in-depth object authorization for user-owned resources."""

    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id
