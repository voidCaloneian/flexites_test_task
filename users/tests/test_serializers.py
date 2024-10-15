from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError
from users.serializers import UserCreateSerializer, UserUpdateSerializer
from users.models import User
from organizations.models import Organization
from users.validators import validate_avatar
from PIL import Image
import tempfile


class UserCreateSerializerTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="Serializer Org",
            description="Organization for serializer tests."
        )

    def test_valid_user_creation(self):
        data = {
            "email": "serializer@example.com",
            "password": "SerializerPass123!",
            "first_name": "Ser",
            "last_name": "Ializer",
            "phone": "+12345678901",
            "organization_ids": [self.organization.id]
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertIn(self.organization, user.organizations.all())

    def test_duplicate_email(self):
        User.objects.create_user(
            email="duplicate@example.com",
            password="DupPass123!",
            first_name="Dup",
            last_name="User"
        )
        data = {
            "email": "duplicate@example.com",
            "password": "AnotherPass123!",
            "first_name": "Another",
            "last_name": "User"
        }
        serializer = UserCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_invalid_password(self):
        data = {
            "email": "invalidpass@example.com",
            "password": "short",
            "first_name": "Invalid",
            "last_name": "Pass"
        }
        serializer = UserCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_avatar_upload(self):
        image = Image.new('RGB', (100, 100), color='blue')
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, format='JPEG')
        tmp_file.seek(0)
        avatar = SimpleUploadedFile(tmp_file.name, tmp_file.read(), content_type='image/jpeg')

        data = {
            "email": "avataruser@example.com",
            "password": "AvatarPass123!",
            "first_name": "Avatar",
            "last_name": "User",
            "avatar": avatar
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertTrue(bool(user.avatar))


class UserUpdateSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="updateuser@example.com",
            password="InitialPass123!",
            first_name="Initial",
            last_name="User"
        )
        self.organization = Organization.objects.create(
            name="Update Org",
            description="Organization for update tests."
        )

    def test_valid_user_update(self):
        data = {
            "first_name": "Updated",
            "last_name": "User",
            "phone": "+19876543210",
            "organization_ids": [self.organization.id]
        }
        serializer = UserUpdateSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.phone, "+19876543210")
        self.assertIn(self.organization, user.organizations.all())

    def test_change_password(self):
        data = {
            "password": "NewSecurePass123!"
        }
        serializer = UserUpdateSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertTrue(user.check_password("NewSecurePass123!"))

    def test_duplicate_email_on_update(self):
        User.objects.create_user(
            email="existing@example.com",
            password="ExistPass123!",
            first_name="Exist",
            last_name="User"
        )
        data = {
            "email": "existing@example.com"
        }
        serializer = UserUpdateSerializer(instance=self.user, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_remove_organizations(self):
        self.user.organizations.add(self.organization)
        data = {
            "organization_ids": []
        }
        serializer = UserUpdateSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.organizations.count(), 0)
