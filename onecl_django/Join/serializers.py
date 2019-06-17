from rest_framework import serializers
from .models import Join
from User.models import CustomUser
from Message.models import Message


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
        previous_level = 0
        modified_level = 0
        if instance.auth_level == 1:
            previous_level = '일반 회원'
        elif instance.auth_level == 2:
            previous_level = '임원'
        if validated_data['auth_level'] == 1:
            modified_level = '일반 회원'
        elif validated_data['auth_level'] == 2:
            modified_level = '임원'
        message_title = '회원님의 <strong>' + instance.club.name + '</strong> 동아리의 회원 등급이 변경되었습니다.'
        message_content = '회원님의 <strong>' + instance.club.name + '</strong> 동아리의 회원 등급이 <strong>' + previous_level + '</strong> 에서 <strong>' + modified_level + '</strong> 으로 변경되었습니다.'
        Message.objects.create(club=instance.club, receiver=instance.user, title=message_title, content=message_content)
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
