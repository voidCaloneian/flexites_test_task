from django.test import TestCase
from organizations.serializers import OrganizationSerializer, UserSerializer
from organizations.models import Organization
from users.models import User


class OrganizationSerializerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@org.com",
            password="Password123!",
            first_name="User",
            last_name="One"
        )
        self.user2 = User.objects.create_user(
            email="user2@org.com",
            password="Password123!",
            first_name="User",
            last_name="Two"
        )
        self.organization = Organization.objects.create(
            name="Serializer Org",
            description="Organization for serializer tests."
        )
        self.organization.users.set([self.user1, self.user2])

    def test_organization_serializer(self):
        serializer = OrganizationSerializer(instance=self.organization)
        data = serializer.data
        self.assertEqual(data['name'], "Serializer Org")
        self.assertEqual(data['description'], "Organization for serializer tests.")
        self.assertEqual(len(data['users']), 2)
        self.assertIn({
            'id': self.user1.id,
            'email': self.user1.email,
            'first_name': self.user1.first_name,
            'last_name': self.user1.last_name
        }, data['users'])
        self.assertIn({
            'id': self.user2.id,
            'email': self.user2.email,
            'first_name': self.user2.first_name,
            'last_name': self.user2.last_name
        }, data['users'])

    def test_create_organization_serializer(self):
        data = {
            "name": "New Org",
            "description": "A new organization."
        }
        serializer = OrganizationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        org = serializer.save()
        self.assertEqual(org.name, "New Org")
        self.assertEqual(org.description, "A new organization.")

    def test_invalid_organization_serializer(self):
        data = {
            "name": "",  # Name is required
            "description": "Missing name."
        }
        serializer = OrganizationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
