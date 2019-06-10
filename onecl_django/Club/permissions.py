from rest_framework import permissions
from User.models import CustomUser


class IsMasterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.method == 'PUT' or request.method == 'DELETE':
            master = CustomUser.objects.get(username=self.request.user.username)
            if obj.master == master:
                return True
        return False



