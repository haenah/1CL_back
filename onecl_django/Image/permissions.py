from rest_framework import permissions
from Join.models import Join
from User.models import CustomUser


class uploadFilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            join = Join.objects.get(club__id=request.GET.get('clubID'), user__username=request.user.username)
            return join.auth_level > 1
        elif request.method == 'POST':
            return True


class FileDetailPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        join = Join.objects.get(club=obj.club, user__username=request.user.username)
        return join.auth_level > 1
