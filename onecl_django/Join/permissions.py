from rest_framework import permissions
from User.models import CustomUser
from Club.models import Club
from Join.models import Join


class JoinListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(username=request.user.username)
        club = None
        if request.method == 'GET':
            club = Club.objects.get(id=request.GET.get('club'))
        elif request.method == 'POST':
            club = Club.objects.get(id=request.data['club'])

        try:
            join = Join.objects.get(user=user, club=club)
        except Join.DoesNotExist:
            return False

        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return join.auth_level > 1


class JoinDetailPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = CustomUser.objects.get(username=request.user.username)
        club = obj.club
        try:
            join = Join.objects.get(user=user, club=club)
        except Join.DoesNotExist:
            return False

        if request.method in ('GET', 'DELETE'):
            return join.user == user or join.auth_level > 1

        if request.method == 'PUT':
            return join.auth_level > 2


class IsMaster(permissions.BasePermission):
    def has_permission(self, request, view):
        club = Club.objects.get(id=request.data['club'])
        user = CustomUser.objects.get(username=request.user.username)
        return club.master == user
