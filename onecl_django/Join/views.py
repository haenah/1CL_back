from rest_framework import permissions, generics, status
from rest_framework.response import Response

from .permissions import *

from .serializers import JoinSerializer
from Join.models import Join
from Club.models import Club
from User.models import CustomUser


# Create your views here.
class JoinList(generics.ListCreateAPIView):
    serializer_class = JoinSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, JoinListPermission)

    def get_queryset(self):
        club = self.request.GET.get('club')
        auth_level = self.request.GET.get('auth_level')
        if club is None or auth_level is None:
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
        user = CustomUser.objects.get(username=self.request.data['user'])
        club = Club.objects.get(id=self.request.data['club'])
        Join.objects.create(user=user, club=club)


class AuthLevelAPI(generics.ListCreateAPIView):
    serializer_class = JoinSerializer

    def get(self, request, *args, **kwargs):
        club = request.GET.get('club')
        user = user = CustomUser.objects.get(username=request.user.username)

        try:
            join = Join.objects.get(user=user, club=club)
        except Join.DoesNotExist:
            body = {"auth_level": 0}
            return Response(body, status=status.HTTP_200_OK)
        body = {"auth_level": join.auth_level}
        return Response(body, status=status.HTTP_200_OK)


class JoinDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Join.objects.all()
    serializer_class = JoinSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, JoinDetailPermission)


