from rest_framework import serializers
from .models import Join
from User.models import CustomUser


class JoinSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    user_name = serializers.ReadOnlyField(source='user.name')
    club = serializers.ReadOnlyField(source='club.id')

    class Meta:
        model = Join
        fields = ('id', 'user_username', 'user_name', 'club', 'auth_level')

    def create(self, validated_data):
        return Join.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.auth_level = validated_data.get('auth_level', instance.auth_level)
        instance.save()
        return instance


class MyClubSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    club_id = serializers.ReadOnlyField(source='club.id')
    club_name = serializers.ReadOnlyField(source='club.name')

    class Meta:
        model = Join
        fields = ('id', 'user', 'club_id', 'club_name', 'auth_level')