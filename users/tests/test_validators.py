from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.validators import validate_avatar
from django.core.exceptions import ValidationError
import tempfile
from PIL import Image


class ValidateAvatarTest(TestCase):
    def create_test_image(self, format='JPEG'):
        with tempfile.NamedTemporaryFile(suffix='.' + format.lower()) as tmp:
            image = Image.new('RGB', (100, 100), color='blue')
            image.save(tmp, format=format)
            tmp.seek(0)
            return SimpleUploadedFile(tmp.name, tmp.read(), content_type=f'image/{format.lower()}')

    def test_valid_avatar_jpeg(self):
        image = self.create_test_image('JPEG')
        try:
            validate_avatar(image)
        except ValidationError:
            self.fail("validate_avatar() raised ValidationError unexpectedly for JPEG.")

    def test_valid_avatar_png(self):
        image = self.create_test_image('PNG')
        try:
            validate_avatar(image)
        except ValidationError:
            self.fail("validate_avatar() raised ValidationError unexpectedly for PNG.")

    def test_invalid_avatar_format(self):
        image = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
        with self.assertRaises(ValidationError):
            validate_avatar(image)

    def test_invalid_avatar_mime_type(self):
        image = self.create_test_image('BMP')  # Assuming BMP is not allowed
        with self.assertRaises(ValidationError):
            validate_avatar(image)
