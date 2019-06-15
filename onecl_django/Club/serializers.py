from rest_framework import serializers
from .models import (Club, Category, Dept)


class ClubSerializer(serializers.ModelSerializer):
    master = serializers.ReadOnlyField(source='master.username')

    class Meta:
        model = Club
        fields = ('id', 'name', 'category', 'dept', 'master', 'apply_message', 'intro')

    def create(self, validated_data):
        return Club.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.master = validated_data.get('master', instance.master)
        instance.category = validated_data.get('category', instance.category)
        instance.dept = validated_data.get('dept', instance.dept)
        instance.apply_message = validated_data.get('apply_message', instance.apply_message)
        instance.intro = validated_data.get('intro', instance.intro)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class DeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dept
        fields = ('name',)
