from rest_framework import permissions
from User.models import CustomUser


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.receiver == CustomUser.objects.get(username=request.user.username)
