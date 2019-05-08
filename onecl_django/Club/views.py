from rest_framework import permissions, generics, status
from django.http import JsonResponse
from .permissions import IsMasterOrBanned
from .serializers import (ClubSerializer, CategorySerializer, DeptSerializer)
from .models import (Club, Category, Dept)


# Create your views here.
class ClubList(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        dept = request.GET.get('department')
        if category==None and dept==None:
            clubs = Club.objects.all()
        elif category=='전체' and dept=='전체':
            clubs = Club.objects.all()
        elif category=='전체':
            clubs = Club.objects.filter(dept=dept)
        elif dept=='전체':
            clubs = Club.objects.filter(category=category)
        elif category!='전체' and dept!= '전체':
            clubs = Club.objects.filter(category=category, dept=dept)
        serializer = ClubSerializer(clubs, many=True)
        return JsonResponse(serializer.data, safe=False)

    def perform_create(self, serializer):
        serializer.save(master=self.request.user)


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
