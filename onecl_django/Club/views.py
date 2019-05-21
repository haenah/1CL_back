from rest_framework import permissions, generics
from Permission.permissions import IsMaster
from .serializers import (ClubSerializer, CategorySerializer, DeptSerializer)
from .models import (Club, Category, Dept)
from User.models import CustomUser
from Join.models import Join


# Create your views here.
class ClubList(generics.ListCreateAPIView):
    serializer_class = ClubSerializer

    def get_queryset(self):
        category = self.request.GET.get('category')
        dept = self.request.GET.get('department')
        if category == None and dept == None:
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


class ClubDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsMaster)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class DeptList(generics.ListAPIView):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
