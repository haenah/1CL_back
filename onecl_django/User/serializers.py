from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("id", "username", "password", "email", "name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "name", "email",)

class DuplicateEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email",)
    #
    # def validate(self, attrs):
    #     UserInfo = CustomUser.objects.all()
    #     for user in UserInfo:
    #         if user.email == attrs['email']:
    #             raise serializers.ValidationError("duplicate email address.")

class DuplicateUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username",)

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")