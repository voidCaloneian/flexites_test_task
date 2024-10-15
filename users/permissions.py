from rest_framework import permissions

class IsStaffOrUserBySelf(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только администраторам или пользователям к своему профилю.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверка прав доступа к объекту.
        :param request:
        :param view:
        :param obj:
        :return:
        """
        return obj == request.user or request.user.is_staff
