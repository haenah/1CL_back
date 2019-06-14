from rest_framework import permissions, generics

from .serializers import DocumentSerializer
from .models import Document
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


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated, DocumentDetailPermission, )
