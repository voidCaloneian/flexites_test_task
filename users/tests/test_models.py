from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User
from organizations.models import Organization


class UserModelTest(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="Test Organization",
            description="A test organization."
        )

    def test_create_user_success(self):
        user = User.objects.create_user(
            email="testuser@example.com",
            password="SecurePassword123!",
            first_name="Test",
            last_name="User"
        )
        user.organizations.add(self.organization)
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("SecurePassword123!"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertIn(self.organization, user.organizations.all())

    def test_create_superuser_success(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="AdminPassword123!",
            first_name="Admin",
            last_name="User"
        )
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertTrue(superuser.check_password("AdminPassword123!"))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_email_unique_constraint(self):
        User.objects.create_user(
            email="unique@example.com",
            password="Password123!",
            first_name="Unique",
            last_name="User"
        )
        with self.assertRaises(ValidationError):
            user = User(
                email="unique@example.com",
                first_name="Duplicate",
                last_name="User"
            )
            user.full_clean()

    def test_phone_validator(self):
        user = User(
            email="phoneuser@example.com",
            password="PhonePass123!",
            first_name="Phone",
            last_name="User",
            phone="+79525295976"
        )
        try:
            user.full_clean()
        except ValidationError as e:
            self.fail("User with valid phone number raised ValidationError.")

        user.phone = "invalid_phone"
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_user_without_organizations(self):
        user = User.objects.create_user(
            email="noorg@example.com",
            password="NoOrgPass123!",
            first_name="NoOrg",
            last_name="User"
        )
        self.assertEqual(user.organizations.count(), 0)
