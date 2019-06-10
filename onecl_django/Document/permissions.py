from rest_framework import permissions
from User.models import CustomUser
from Join.models import Join
from Club.models import Club


class DocumentListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(username=self.request.user.username)
        if request.method == 'GET':
            club = Club.objects.get(id=self.request.GET.get('club'))
            return Join.objects.filter(user=user).filter(club=club).exists()
        if request.method == 'POST':
            join = Join.objects.get(user=user, club=request.data['club'])
            if self.request.data['type'] == 'notice':
                if join.auth_level >= 2:
                    return True
            else:
                return True
        return False


class DocumentDetailPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = CustomUser.objects.get(username=self.request.user.username)
        club = Club.objects.get(id=obj.club.id)
        try:
            join = Join.objects.get(user=user, club=club)
        except join.DoesNotExist:
            return False

        if request.method == 'GET':
            return True
        if request.method == 'PUT':
            return user == obj.owner
        if request.method == 'DELETE':
            return user == obj.owner or join.auth_level >= 2
        return False
