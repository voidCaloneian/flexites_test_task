from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from organizations.models import Organization
from .models import User
from .validators import validate_avatar


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Organization.
    Используется для отображения подробной информации об организациях.
    """

    class Meta:
        model = Organization
        fields = ['id', 'name', 'description']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователя.
    Обрабатывает создание пользователя с установкой пароля и привязкой организаций.
    """
    organization_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Organization.objects.all(),
        required=False,
        help_text="Список ID организаций для привязки к пользователю."
    )
    organizations = OrganizationSerializer(many=True, read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="Пароль пользователя."
    )
    avatar = serializers.ImageField(
        required=False,
        validators=[validate_avatar],
        help_text="Аватар пользователя."
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
            'avatar',
            'organization_ids',
            'organizations',
        ]

    def validate_email(self, value):
        """
        Проверка уникальности email.

        :param value: Проверяемое email
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        """
        Создает нового пользователя с привязкой к организациям.
        """
        organizations = validated_data.pop('organization_ids', [])
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if organizations:
            user.organizations.set(organizations)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления информации о пользователе.
    Позволяет обновлять информацию и изменять привязку к организациям.
    """
    organization_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Organization.objects.all(),
        write_only=True,
        required=False,
        help_text="Список ID организаций для привязки к пользователю."
    )
    organizations = OrganizationSerializer(many=True, read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="Новый пароль пользователя."
    )
    avatar = serializers.ImageField(
        required=False,
        validators=[validate_avatar],  # Если вы добавили кастомный валидатор для аватарок
        help_text="Новый аватар пользователя."
    )

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
            'avatar',
            'organization_ids',
            'organizations',
        ]

    def validate_email(self, value):
        """
        Проверка уникальности email при обновлении.
        """
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Обновляет информацию о пользователе и привязку к организациям.
        """
        organizations = validated_data.pop('organization_ids', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        if organizations is not None:
            instance.organizations.set(organizations)

        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального отображения информации о пользователе.
    Отображает подробную информацию об организациях.
    """
    organizations = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'avatar',
            'organizations',
            'is_active',
            'is_staff',
            'date_joined',
        ]
        read_only_fields = [
            'id',
            'is_active',
            'is_staff',
            'date_joined',
            'organizations',
        ]
