from rest_framework import serializers
from .models import Join


class JoinSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    club = serializers.ReadOnlyField(source='club')

    class Meta:
        model = Join
        fields = ('id', 'user', 'club', 'auth_level')

    def create(self, validated_data):
        return Join.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.auth_level = validated_data['auth_level']
        instance.save()
        return instance


class MyClubSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    club_id = serializers.ReadOnlyField(source='club.id')
    club_name = serializers.ReadOnlyField(source='club.name')

    class Meta:
        model = Join
        fields = ('id', 'user', 'club', 'club_name', 'auth_level')
