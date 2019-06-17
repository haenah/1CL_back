from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from .serializers import MessageSerializer
from .models import Message
from User.models import CustomUser
from .permissions import *
from rest_framework.response import Response


# Create your views here.
class MessageList(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = CustomUser.objects.get(username=self.request.user.username)
        return Message.objects.filter(receiver=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MessageDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            body = {"message": "Requested objected does not exist."}
            return Response(body, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        message = self.get_object(pk)
        message.read = True
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        body = {"message":"cannot modify message's title or content"}
        return Response(body, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        document = self.get_object(pk)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteReadMessage(generics.GenericAPIView):
    def get_queryset(self):
        return Message.objects.filter(receiver__username=self.request.user.username, read=True)

    def get(self, request, *args, **kwargs):
        message_read = self.get_queryset()
        for message in message_read:
            message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


