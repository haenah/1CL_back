from .models import ImageModel, FileModel
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ImageUploadSerializer, FileUploadSerializer
from User.models import CustomUser
from Club.models import Club
from Message.models import Message
from rest_framework.views import APIView


class uploadImageAPI(generics.ListCreateAPIView):
    serializer_class = ImageUploadSerializer
    queryset = ImageModel.objects.all()

    def post(self, request, *args, **kwargs):

        clubID = request.GET.get('clubID')
        club = Club.objects.get(id=clubID)
        newImage = ImageModel(image=self.request.FILES['upload'], club=club, name=self.request.FILES['upload'].name)
        newImage.save()

        return Response(
            {
                "image": ImageUploadSerializer(
                    self.request.FILES['upload'], context=self.get_serializer_context()
                ).data,
            }
        )

    def get_queryset(self):
        club = self.request.GET.get('clubID')
        if club is None:
            return ImageModel.objects.all()
        return ImageModel.objects.filter(club=club)

    # def perform_create(self, serializer):
    #     user = CustomUser.objects.get(username=self.request.user.username)
    #     club = Club.objects.get(id=self.request.GET.get('id'))
    #     serializer.save(user=user, club=club, name=self.request.FILES['file'].name)

class uploadFileAPI(generics.ListCreateAPIView):
    serializer_class = FileUploadSerializer
    queryset = FileModel.objects.all()

    def post(self, request, *args, **kwargs):
        thisUser = CustomUser.objects.get(username=request.user.username)
        club = Club.objects.get(id=request.GET.get('clubID'))

        uploadedList = FileModel.objects.filter(club=club).filter(user=thisUser)

        for file in uploadedList:
            if file.club == club and file.user.username == request.user.username:
                body = {"message": "duplicate uploader"}
                return Response(body, status.HTTP_400_BAD_REQUEST)

        newFile = FileModel(file=self.request.FILES['file'], name=self.request.FILES['file'].name, user=thisUser, club=club)
        newFile.save()

        return Response(status=status.HTTP_201_CREATED)

    def get_queryset(self):
        club = self.request.GET.get('clubID')
        if club is None:
            return FileModel.objects.all()
        return FileModel.objects.filter(club=club)


class FileDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = FileModel.objects.all()
    serializer_class = FileUploadSerializer


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return FileModel.objects.get(pk=pk)
        except FileModel.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileUploadSerializer(file)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileUploadSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        if request.data['apply'] == 'true':
            message_title = '<strong>' + file.club.name + '</strong> 동아리 가입이 승인되었습니다.'
            message_content = message_title + ' 동아리 가입을 진심으로 환영합니다!'
            Message.objects.create(club=file.club, receiver=file.user, title=message_title, content=message_content)
        elif request.data['apply'] == 'false':
            message_title = '<strong>' + file.club.name + '</strong> 동아리 가입이 반려되었습니다.'
            message_content = message_title + '함께하지 못하게 되어 죄송합니다.'
            Message.objects.create(club=file.club, receiver=file.user, title=message_title, content=message_content)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
