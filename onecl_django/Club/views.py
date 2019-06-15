from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (ClubSerializer, CategorySerializer, DeptSerializer)
from .models import (Club, Category, Dept)
from User.models import CustomUser
from Join.models import Join
from .permissions import IsMasterOrReadOnly


# Create your views here.
class ClubList(generics.ListCreateAPIView):
    serializer_class = ClubSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        category = self.request.GET.get('category')
        dept = self.request.GET.get('department')
        if category is None and dept is None:
            return Club.objects.all()
        elif category == '전체' and dept == '전체':
            return Club.objects.all()
        elif category == '전체':
            return Club.objects.filter(dept=dept)
        elif dept == '전체':
            return Club.objects.filter(category=category)
        elif category != '전체' and dept != '전체':
            return Club.objects.filter(category=category, dept=dept)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        master = CustomUser.objects.get(username=self.request.user.username)
        Join.objects.create(user=master, club=serializer.save(master=master), auth_level=3)


class ClubDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            body = {"message":"Requested club does not exist."}
            return Response(body, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        club = self.get_object(pk)
        serializer = ClubSerializer(club)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        club = self.get_object(pk)
        new_data = request.data

        if request.data['intro'] is not None:
            new_data['name'] = club.name
            new_data['category'] = club.category
            new_data['dept'] = club.dept
            new_data['apply_message'] = club.apply_message

        else:
            new_data['intro'] = club.intro

        serializer = ClubSerializer(club, data=new_data)
        if serializer.is_valid():
            serializer.save()
            print('haha')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class DeptList(generics.ListAPIView):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
