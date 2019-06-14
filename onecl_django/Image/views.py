from .models import ImageModel, FileModel
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ImageUploadSerializer, FileUploadSerializer
from User.models import CustomUser
from Club.models import Club


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
