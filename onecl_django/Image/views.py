from .models import ImageModel
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from .serializers import ImageUploadSerializer

class uploadImageAPI(generics.ListCreateAPIView):
    serializer_class = ImageUploadSerializer
    queryset = ImageModel.objects.all()

    def post(self, request, *args, **kwargs):

        newImage = ImageModel(image=self.request.FILES['upload'])
        newImage.save()

        return Response(
            {
                "image": ImageUploadSerializer(
                    self.request.FILES['upload'], context=self.get_serializer_context()
                ).data,
            }
        )

    # def create(self, request, *args, **kwargs):
    #     return Response(
    #         {
    #             "data": ImageUploadSerializer(
    #                 self.request.FILES['upload'], context=self.get_serializer_context()
    #             ).data
    #         }
    #     )

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = ImageUploadSerializer

