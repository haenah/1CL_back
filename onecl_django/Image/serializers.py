from rest_framework import serializers
from .models import ImageModel

class ImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageModel
        fields = ("id", "image",)

    def create(self, validated_data):
        return ImageModel.objects.create(**validated_data)
