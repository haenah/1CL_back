from rest_framework import permissions
from User.models import CustomUser
from Club.models import Club
from Join.models import Join


class JoinListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(username=self.request.user.username)
        club = Club.objects.get(id=self.request.GET.get('club'))
        try:
            join = Join.objects.get(user=user, club=club)
        except join.DoesNotExist:
            return False

        if request.method == 'GET':
            return True
        if request.method == 'POST':
            if self.request.data['type'] == 'notice':
                if join.auth_level >= 2:
                    return True
            else:
                return True
        return False