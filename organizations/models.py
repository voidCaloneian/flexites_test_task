from django.db import models

class Organization(models.Model):
    """Модель организации."""
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Краткое описание', blank=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        """Строковое представление организации."""
        return self.name
