from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from organizations.models import Organization
from users.models import User
from django.contrib.auth import get_user_model


class OrganizationViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email="admin@org.com",
            password="AdminPass123!",
            first_name="Admin",
            last_name="User"
        )
        self.user = User.objects.create_user(
            email="user@org.com",
            password="UserPass123!",
            first_name="Regular",
            last_name="User"
        )
        self.organization = Organization.objects.create(
            name="Existing Org",
            description="An existing organization."
        )
        self.organization.users.set([self.user])

    def authenticate_as_admin(self):
        self.client.force_authenticate(user=self.admin)

    def authenticate_as_user(self):
        self.client.force_authenticate(user=self.user)

    def test_create_organization_as_admin(self):
        self.authenticate_as_admin()
        url = reverse('organization-list')  # Убедитесь, что маршрутизатор использует это имя
        data = {
            "name": "Admin Created Org",
            "description": "Created by admin."
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 2)
        self.assertEqual(Organization.objects.get(id=response.data['id']).name, "Admin Created Org")

    def test_create_organization_as_non_admin(self):
        self.authenticate_as_user()
        url = reverse('organization-list')
        data = {
            "name": "User Created Org",
            "description": "Attempted creation by non-admin."
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_organizations_as_admin(self):
        self.authenticate_as_admin()
        url = reverse('organization-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_organizations_as_authenticated_user(self):
        self.authenticate_as_user()
        url = reverse('organization-list')
        response = self.client.get(url, format='json')
        # Предположим, что все аутентифицированные пользователи могут просматривать организации
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_organization(self):
        self.authenticate_as_user()
        url = reverse('organization-detail', args=[self.organization.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Existing Org")
        self.assertEqual(len(response.data['users']), 1)

    def test_update_organization_as_admin(self):
        self.authenticate_as_admin()
        url = reverse('organization-detail', args=[self.organization.id])
        data = {
            "name": "Updated Org",
            "description": "Updated description."
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.name, "Updated Org")
        self.assertEqual(self.organization.description, "Updated description.")

    def test_update_organization_as_non_admin(self):
        self.authenticate_as_user()
        url = reverse('organization-detail', args=[self.organization.id])
        data = {
            "name": "Hacked Org",
            "description": "Hacked description."
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_organization_as_admin(self):
        self.authenticate_as_admin()
        url = reverse('organization-detail', args=[self.organization.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Organization.objects.filter(id=self.organization.id).exists())

    def test_delete_organization_as_non_admin(self):
        self.authenticate_as_user()
        url = reverse('organization-detail', args=[self.organization.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
