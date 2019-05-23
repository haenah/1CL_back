from rest_framework import permissions
from User.models import CustomUser
from Join.models import Join


class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        join = Join.objects.get(username=request.user.username, club=request.GET.get('club'))
        return join.auth_level >= 1


class IsExecutive(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        join = Join.objects.get(username=request.user.username, club=request.GET.get('club'))
        return join.auth_level >= 2


class IsMaster(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        join = Join.objects.get(username=request.user.username, club=request.GET.get('club'))
        return join.auth_level == 3


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = CustomUser.objects.get(username=request.user.username)
        return obj.user == user
