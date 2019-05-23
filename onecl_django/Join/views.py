from rest_framework import permissions, generics
from Permission.permissions import IsSelf, IsMember, IsExecutive
from .serializers import JoinSerializer
from Join.models import Join
from Club.models import Club
from User.models import CustomUser


# Create your views here.
class JoinList(generics.ListCreateAPIView):
    serializer_class = JoinSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsMember)

    def get_queryset(self):
        club = self.request.GET.get('club')
        auth_level = self.request.GET.get('auth_level')
        if club == None or auth_level == None:
            return Join.objects.all()
        elif auth_level == 1:
            return Join.objects.filter(club=club)
        elif auth_level == 2:
             Join.objects.filter(club=club, auth_level__gte=2)
        elif auth_level == 3:
            return Join.objects.filter(club=club, auth_level=3)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = CustomUser.objects.get(id=self.request.GET.get('user'))
        club = Club.objects.get(id=self.request.GET.get('club'))
        Join.objects.create(user=user, club=club)


class JoinDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Join.objects.all()
    serializer_class = JoinSerializer
    permission_classes = (IsSelf, IsExecutive)


