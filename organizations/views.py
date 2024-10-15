from rest_framework import viewsets, permissions
from .models import Organization
from .serializers import OrganizationSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления организациями.

    Доступные действия:
    - list: Список всех организаций
    - retrieve: Получение детальной информации об организации
    И так далее... (остальное по ТЗ не требовалось)
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        """
        Возвращает список разрешений в зависимости от действия.
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]
