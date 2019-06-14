from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = Document
        fields = ('id', 'title', 'content', 'date', 'owner', 'club')

    def create(self, validated_data):
        return Document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('name', instance.title)
        instance.content = validated_data.get('master', instance.content)
        instance.type = validated_data.get('category', instance.type)
        instance.save()
        return instance

