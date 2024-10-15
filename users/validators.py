from django.core.exceptions import ValidationError


def validate_avatar(image):
    """
    Валидатор для проверки аватарки.
    Проверяет размер файла и тип изображения.

    :param image: Загруженное изображение
    """

    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif, image/jpg', 'image/webp']
    if image.content_type not in valid_mime_types:
        raise ValidationError("Неверный тип изображения. Разрешены JPEG, PNG, GIF и WEBP.")
