from rest_framework import serializers
from .models import Document, DocumentType


class DocumentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.name')
    view = serializers.ReadOnlyField(source='view')
    type_name = serializers.ReadOnlyField(source='type.name')

    class Meta:
        model = Document
        fields = ('id', 'title', 'type', 'type_name', 'content', 'date', 'owner', 'club', 'view')

    def create(self, validated_data):
        return Document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.club = validated_data.get('club', instance.club)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'name', 'club')

    def create(self, validated_data):
        return DocumentType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.club = validated_data.get('club', instance.club)
        instance.save()
        return instance
