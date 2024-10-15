from django.test import TestCase
from organizations.models import Organization


class OrganizationModelTest(TestCase):
    def test_create_organization_success(self):
        org = Organization.objects.create(
            name="Test Organization",
            description="A test organization."
        )
        self.assertEqual(org.name, "Test Organization")
        self.assertEqual(org.description, "A test organization.")

    def test_str_representation(self):
        org = Organization.objects.create(
            name="Str Org",
            description="Testing __str__ method."
        )
        self.assertEqual(str(org), "Str Org")

    def test_name_max_length(self):
        name = 'A' * 100
        org = Organization(name=name)
        try:
            org.full_clean()
        except Exception as e:
            self.fail(f"Organization with name length 100 raised an exception: {e}")

        org.name = 'A' * 101
        with self.assertRaises(Exception):
            org.full_clean()
