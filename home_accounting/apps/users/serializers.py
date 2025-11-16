# apps/users/serializers.py
from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "gender", "avatar", "is_parent")

class FamilySerializer(serializers.Serializer):
    # В данном приложении Family модель будет добавлена позже, сериализатор можно расширить
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    members = serializers.ListField(child=serializers.CharField(), read_only=True)
