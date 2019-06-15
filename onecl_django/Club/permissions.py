from rest_framework import permissions
from User.models import CustomUser


class IsMasterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        master = CustomUser.objects.get(username=request.user.username)
        return master == obj.master
