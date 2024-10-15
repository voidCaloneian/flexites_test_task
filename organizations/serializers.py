from rest_framework import serializers
from users.models import User
from .models import Organization


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    Отображает основные поля пользователя.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Organization.
    Включает связанных пользователей.
    """
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'users']
