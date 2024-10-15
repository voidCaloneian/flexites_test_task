from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from organizations.models import Organization
from django.urls import reverse


class IsStaffOrUserBySelfPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.organization = Organization.objects.create(
            name="Permission Org",
            description="Organization for permission tests."
        )
        self.user = User.objects.create_user(
            email="userperm@example.com",
            password="UserPerm123!",
            first_name="User",
            last_name="Perm"
        )
        self.admin = User.objects.create_superuser(
            email="adminperm@example.com",
            password="AdminPerm123!",
            first_name="Admin",
            last_name="Perm"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="OtherPass123!",
            first_name="Other",
            last_name="User"
        )

    def test_permission_as_self(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_as_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_update_as_self(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user-detail', args=[self.user.id])
        data = {"first_name": "NewName"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "NewName")

    def test_permission_update_as_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('user-detail', args=[self.user.id])
        data = {"first_name": "HackedName"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
