from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import *
from .serializers import *
from Join.models import Join
from Club.models import Club
from User.models import CustomUser
from Message.models import Message


# Create your views here.
class JoinList(generics.ListCreateAPIView):
    serializer_class = JoinSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, JoinListPermission)

    def get_queryset(self):
        club = self.request.GET.get('club')
        auth_level = self.request.GET.get('auth_level')
        if club is None or auth_level is None:
            return Join.objects.all()
        elif auth_level == '1':
            return Join.objects.filter(club=club)
        elif auth_level == '2':
             Join.objects.filter(club=club, auth_level__gte=2)
        elif auth_level == '3':
            return Join.objects.filter(club=club, auth_level=3)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = CustomUser.objects.get(username=self.request.data['user'])
        club = Club.objects.get(id=self.request.data['club'])
        Join.objects.create(user=user, club=club)
        # message_title = '<strong>'+club.name+'</strong> 동아리 가입이 승인되었습니다.'
        # message_content = message_title+' 동아리 가입을 진심으로 환영합니다!'
        # Message.objects.create(club=club, receiver=user, title=message_title, content=message_content)


class AuthLevelAPI(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, *args, **kwargs):
        club = Club.objects.get(id=request.GET.get('club'))

        try:
            user = CustomUser.objects.get(username=request.user.username)
        except Exception:
            body = {"auth_level": -1}
            return Response(body, status=status.HTTP_200_OK)

        try:
            join = Join.objects.get(user=user, club=club)
        except Join.DoesNotExist:
            body = {"auth_level": 0}
            return Response(body, status=status.HTTP_200_OK)
        body = {"auth_level": join.auth_level}
        return Response(body, status=status.HTTP_200_OK)


class MyClubList(generics.ListCreateAPIView):
    serializer_class = MyClubSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        user = CustomUser.objects.get(username=self.request.user.username)
        return Join.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class JoinDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, JoinDetailPermission)

    def get_object(self, pk):
        try:
            return Join.objects.get(pk=pk)
        except Join.DoesNotExist:
            body = {"message": "Requested objected does not exist."}
            return Response(body, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        join = self.get_object(pk)
        serializer = JoinSerializer(join)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        join = self.get_object(pk)
        previous_level = 0
        modified_level = 0
        if join.auth_level == 1:
            previous_level = '일반 회원'
        elif join.auth_level == 2:
            previous_level = '임원'
        if request.data['auth_level'] == 1:
            modified_level = '일반 회원'
        elif request.data['auth_level'] == 2:
            modified_level = '임원'
        message_title = '회원님의 <strong>' + join.club.name + '</strong> 동아리의 회원 등급이 변경되었습니다.'
        message_content = '회원님의 <strong>' + join.club.name + '</strong> 동아리의 회원 등급이 <strong>' + previous_level + '</strong> 에서 <strong>' + modified_level + '</strong> 으로 변경되었습니다.'
        Message.objects.create(club=join.club, receiver=join.user, title=message_title, content=message_content)
        serializer = JoinSerializer(join, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        document = self.get_object(pk)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchUserAPI(generics.ListAPIView):
    serializer_class = JoinSerializer
    permission_classes = (IsMaster, )

    def get_queryset(self):
        return Join.objects.filter(club=self.request.GET.get('club')).filter(user__name__startswith=self.request.GET.get('name'))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DelegateMaster(generics.GenericAPIView):
    serializer_class = JoinSerializer
    permission_classes = (IsMaster, )

    def put(self, request, *args, **kwargs):
        previousMaster = Join.objects.get(user__username=request.user.username, club=request.data['club'])
        newMaster = Join.objects.get(user__username=request.data['username'], club=request.data['club'])
        previousMaster.auth_level = 1
        newMaster.auth_level = 3
        club = Club.objects.get(id=request.data['club'])
        club.master = newMaster.user
        previousMaster.save()
        newMaster.save()
        club.save()

        message_title = '<strong>'+club.name+'</strong> 동아리의 회장 권한이 위임되었습니다.'
        message_content = '<strong>'+club.name+'</strong> 동아리의 회장 권한이 <strong>'+previousMaster.user.name+'</strong> 에서 <strong>'+newMaster.user.name+'</strong> 으로 위임되었습니다.'
        members = Join.objects.filter(club=club)
        for member in members:
            Message.objects.create(club=club, receiver=member.user, title=message_title, content=message_content)

        body = {"message":"delegation completed."}
        return Response(body, status=status.HTTP_200_OK)
