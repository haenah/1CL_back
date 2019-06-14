from rest_framework import serializers
from .models import ImageModel, FileModel

class ImageUploadSerializer(serializers.ModelSerializer):
    # club = serializers.ReadOnlyField(source='Club.id')

    class Meta:
        model = ImageModel
        fields = ("id", "name", "image", "club")

    def create(self, validated_data):
        return ImageModel.objects.create(**validated_data)

class FileUploadSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FileModel
        fields = ("id", "name", "file", "user", "club")

    def create(self, validated_data):
        return FileModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.user = validated_data.get('user', instance.user)
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance
