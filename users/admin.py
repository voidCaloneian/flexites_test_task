from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Пользовательский интерфейс администратора для модели User.
    """
    # Отображение полей в форме пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'phone', 'avatar', 'organizations')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    # Отображение полей в списке пользователей
    list_display = ('email', 'first_name', 'last_name')
    # Поля, по которым можно будет искать пользователей
    search_fields = ('email', 'first_name', 'last_name')
    # Упорядочивание пользователей по email
    ordering = ('email',)
