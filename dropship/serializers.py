from pyexpat import model
from rest_framework import serializers
from .models import Project, Issue, Member
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def create(self, validated_data):
        user = Member.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_admin=validated_data['is_admin'],
            is_manager=validated_data['is_manager']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True, write_only=True)


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'