from django.db.models import Q
from rest_framework import permissions, generics, mixins
from .serializers import DocumentSerializer, DocumentTypeSerializer
from .models import Document, DocumentType
from .permissions import *

# Create your views here.
class DocumentList(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated, DocumentListPermission )

    def get_queryset(self):
        club = self.request.GET.get('club')
        title = self.request.GET.get('title')
        content = self.request.GET.get('content')
        owner = self.request.GET.get('owner')
        type = self.request.GET.get('type')

        result = Document.objects.filter(club=club)

        if type != '전체':
            result = result.filter(type=type)
        if title is not None:
            result = result.filter(title=title)
        if content is not None:
            result = result.filter(content=content)
        if owner is not None:
            user = CustomUser.objects.get(username=owner)
            result = result.filter(owner=user)

        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        owner = CustomUser.objects.get(username=self.request.user.username)
        serializer.save(owner=owner)


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class DocumentTypeList(generics.ListCreateAPIView):
    serializer_class = DocumentTypeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        club = self.request.query_params.get('club')
        return DocumentType.objects.filter(Q(club=club) | Q(club=None))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(type=type)


class DocumentTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentType.objects.exclude(club=None)
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated, )
