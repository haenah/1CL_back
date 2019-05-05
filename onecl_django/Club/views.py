from rest_framework import permissions, generics
from .permissions import IsMasterOrBanned
from .serializers import (ClubSerializer, CategorySerializer, DeptSerializer)
from .models import (Club, Category, Dept)
from User.models import CustomUser


# Create your views here.
class ClubList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    def perform_create(self, serializer):
        serializer.save(master=self.request.user)

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class ClubDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsMasterOrBanned)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class DeptList(generics.ListAPIView):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
