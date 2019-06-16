from rest_framework import permissions, generics
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
