import os
import random
import string
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator, validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from PIL import Image


def generate_random_filename(length=10):
    """
    Генерирует случайное имя файла из букв и цифр.
    Структура имени: <length> случайных символов [a-zA-Z0-9].

    :param length: Длина имени файла
    :return: Случайное имя файла
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def avatar_upload_path(instance, filename):
    """
    Определяет путь для загрузки аватара пользователя.
    Структура пути: avatars/<случайное_имя>.<расширение>
    Проверяет уникальность имени файла и генерирует новое имя при необходимости.

    :param instance: Экземпляр модели пользователя (Не используется)
    :param filename: Имя загружаемого файла
    :return: Путь для загрузки файла
    """
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    allowed_extensions = getattr(settings, 'ALLOWED_AVATAR_EXTENSIONS', ['.jpg', '.jpeg', '.png', '.gif'])
    if extension not in allowed_extensions:
        extension = '.jpg'  # Используем расширение по умолчанию, если расширение не разрешено

    upload_dir = getattr(settings, 'AVATAR_UPLOAD_DIR', 'avatars/')
    max_attempts = 5  # Максимальное количество попыток генерации уникального имени

    for _ in range(max_attempts):
        new_filename = generate_random_filename()
        full_path = os.path.join(upload_dir, f"{new_filename}{extension}")
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, full_path)):
            return full_path
        # Если файл существует, пробуем сгенерировать новое имя

    # Если все попытки не увенчались успехом, генерируем уникальное имя с помощью UUID
    unique_filename = f"{uuid.uuid4().hex}{extension}"
    return os.path.join(upload_dir, unique_filename)


class CustomUserManager(BaseUserManager):
    """Менеджер модели пользователя с методами для создания пользователей и суперпользователей."""

    def create_user(self, email, password, **extra_fields):
        """
        Создаёт и сохраняет пользователя с указанным email и паролем.

        :param email: Электронная почта пользователя
        :param password: Пароль пользователя
        :param extra_fields: Дополнительные поля модели пользователя
        :return: Созданный пользователь
        """
        if not email:
            raise ValueError('Email должен быть указан')
        if not password:
            raise ValueError('Пароль должен быть указан')

        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('Неверный формат email адреса')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создаёт и сохраняет суперпользователя с указанным email и паролем.

        :param email: Электронная почта суперпользователя
        :param password: Пароль суперпользователя
        :param extra_fields: Дополнительные поля модели пользователя
        :return: Созданный суперпользователь
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя."""

    email = models.EmailField(_('Email'), unique=True)
    first_name = models.CharField(_('Имя'), max_length=30)
    last_name = models.CharField(_('Фамилия'), max_length=30)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Телефонный номер должен быть в формате: '+999999999'. До 15 цифр.")
    )
    phone = models.CharField(_('Телефон'), max_length=20, blank=True, validators=[phone_regex])
    avatar = models.ImageField(_('Аватар'), upload_to=avatar_upload_path, blank=True, null=True)
    organizations = models.ManyToManyField(
        'organizations.Organization',
        verbose_name=_('Организации'),
        blank=True,
        related_name='users'
    )
    is_active = models.BooleanField(_('Активный'), default=True)
    is_staff = models.BooleanField(_('Сотрудник'), default=False)
    date_joined = models.DateTimeField(_('Дата регистрации'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']

    def __str__(self):
        """Строковое представление пользователя."""
        return f"{self.email} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """
        Переопределяет метод сохранения для обработки аватара после сохранения объекта.
        Использует обработку исключений для предотвращения сбоев при ошибках обработки изображения.
        """
        super().save(*args, **kwargs)
        if self.avatar:
            try:
                self.resize_avatar()
            except Exception:
                pass

    def resize_avatar(self):
        """
        Изменяет размер аватара до 200x200 пикселей, сохраняя качество и оптимизируя изображение.
        """
        with Image.open(self.avatar.path) as image:
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            image.thumbnail(settings.AVATAR_MAX_SIZE)
            image.save(self.avatar.path, optimize=True, quality=settings.AVATAR_QUALITY)

