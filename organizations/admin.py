from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Пользовательский интерфейс администратора для модели Organization.
    """
    list_display = ('name',)
    search_fields = ('name',)
