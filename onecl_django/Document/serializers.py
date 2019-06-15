from rest_framework import serializers
from .models import Document, DocumentType, Comment


class DocumentSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.name')
    owner_username = serializers.ReadOnlyField(source='owner.username')
    view = serializers.ReadOnlyField()
    type_name = serializers.ReadOnlyField(source='type.name')

    class Meta:
        model = Document
        fields = ('id', 'title', 'type', 'type_name', 'content', 'date', 'owner_name', 'owner_username', 'club', 'view')

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


class CommentSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.name')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'content', 'owner_name', 'owner_username', 'document', 'date')

    def create(self, valdated_data):
        return Comment.objects.create(**valdated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
