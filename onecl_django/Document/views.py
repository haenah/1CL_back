from django.db.models import Q
from rest_framework import permissions, generics, status
from .serializers import *
from .models import *
from User.models import CustomUser
from .permissions import *
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class DocumentList(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated, DocumentListPermission)

    def get_queryset(self):
        club = self.request.GET.get('club')
        title = self.request.GET.get('title')
        content = self.request.GET.get('content')
        owner = self.request.GET.get('owner')
        type = self.request.GET.get('type')

        result = Document.objects.filter(club=club)

        if type != 'all':
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


class DocumentDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, DocumentDetailPermission, )

    def get_object(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            body = {"message": "Requested objected does not exist."}
            return Response(body, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        document = self.get_object(pk)
        document.view += 1
        document.save()
        serializer = DocumentSerializer(document)
        result = {}
        result['document'] = serializer.data
        result['comments'] = CommentSerializer(Comment.objects.filter(document=document.id), many=True).data
        return Response(result)

    def put(self, request, pk, format=None):
        document = self.get_object(pk)
        serializer = DocumentSerializer(document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        document = self.get_object(pk)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentTypeList(generics.ListCreateAPIView):
    serializer_class = DocumentTypeSerializer
    permission_classes = (permissions.IsAuthenticated, DocumentTypeListPermission)

    def get_queryset(self):
        club = self.request.query_params.get('club')
        return DocumentType.objects.filter(Q(club=club) | Q(club=None))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()


class DocumentTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentType.objects.exclude(club=None)
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated, DocumentTypeDetailPermission)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, CommentListPermission, )

    def perform_create(self, serializer):
        owner = CustomUser.objects.get(username=self.request.user.username)
        serializer.save(owner=owner)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, CommentDetailPermission, )
