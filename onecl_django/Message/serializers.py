from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    club_id = serializers.ReadOnlyField(source='club.id')
    club_name = serializers.ReadOnlyField(source='club.name')
    receiver = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ('id', 'club_id', 'club_name', 'receiver', 'title', 'content', 'date', 'read')

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
