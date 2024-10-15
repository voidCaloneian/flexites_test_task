from rest_framework import viewsets, permissions
from .models import User
from .serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserDetailSerializer
)
from .permissions import IsStaffOrUserBySelf  # Убедитесь, что имя класса корректно


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.

    Доступные действия:
    - list: Список всех пользователей (только для администраторов)
    - create: Создание нового пользователя (доступно всем)
    - retrieve: Получение детальной информации о пользователе
    - update: Полное обновление пользователя
    - partial_update: Частичное обновление пользователя
    - destroy: Удаление пользователя (только для администраторов)
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'list':
            return UserDetailSerializer
        return UserDetailSerializer

    def get_permissions(self):
        """
        Возвращает список разрешений в зависимости от действия.
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsStaffOrUserBySelf()]
        else:
            return [permissions.IsAdminUser()]
