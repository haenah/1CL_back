from rest_framework import permissions, generics

from .serializers import DocumentSerializer
from .models import Document, DocumentType
from User.models import CustomUser
from Club.models import Club
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
        if title is not None:
            return Document.objects.filter(club=club, title=title)
        if content is not None:
            return Document.objects.filter(club=club, content=content)
        if owner is not None:
            user = CustomUser.objects.get(username=owner)
            return Document.objects.filter(club=club, owner=user)
        if type is not None:
            return Document.objects.filter(club=club, type=type)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        owner = CustomUser.objects.get(username=self.request.user.username)
        serializer.save(owner=owner)


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated, DocumentDetailPermission, )


class DocumentTypeList(generics.ListCreateAPIView):
    def get_queryset(self):
        return None
