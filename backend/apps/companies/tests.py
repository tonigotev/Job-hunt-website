from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from companies.models import Company

User = get_user_model()


class CompanyTests(APITestCase):
    def setUp(self):
        # Create users
        self.company_user_1 = User.objects.create_user(
            username="company1",
            password="Password123",
            email="company1@example.com",
            role="company",
            first_name="Company",
            last_name="One",
        )
        self.company_user_2 = User.objects.create_user(
            username="company2",
            password="Password123",
            email="company2@example.com",
            role="company",
        )
        self.admin_user = User.objects.create_superuser(
            username="admin", password="Password123", email="admin@example.com", role="admin"
        )
        self.seeker_user = User.objects.create_user(
            username="seeker", password="Password123", email="seeker@example.com", role="job_seeker"
        )

        # Company profiles are created automatically via signals/user creation logic
        self.company_1 = Company.objects.get(user=self.company_user_1)
        self.company_2 = Company.objects.get(user=self.company_user_2)

        # URLs
        self.my_company_url = reverse("companies:company-my-company")
        self.company_detail_url = reverse(
            "companies:company-detail", kwargs={"pk": self.company_1.pk}
        )

    def test_get_my_company_successful(self):
        """A company user can retrieve their own profile."""
        self.client.force_authenticate(user=self.company_user_1)
        response = self.client.get(self.my_company_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], self.company_user_1.email)

    def test_update_my_company_successful(self):
        """A company user can update their own profile."""
        self.client.force_authenticate(user=self.company_user_1)
        update_data = {"website": "https://new-website.com"}
        response = self.client.patch(self.my_company_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company_1.refresh_from_db()
        self.assertEqual(self.company_1.website, "https://new-website.com")

    def test_job_seeker_cannot_access_my_company_endpoint(self):
        """A job seeker should get a 404 from the my-company endpoint."""
        self.client.force_authenticate(user=self.seeker_user)
        response = self.client.get(self.my_company_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_company_cannot_update_profile(self):
        """A company user CANNOT update another company's profile."""
        self.client.force_authenticate(user=self.company_user_2)
        update_data = {"title": "Malicious Title"}
        response = self.client.patch(self.company_detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_update_profile(self):
        """A company user CAN update their own profile via the detail URL."""
        self.client.force_authenticate(user=self.company_user_1)
        update_data = {"description": "An updated description."}
        response = self.client.patch(self.company_detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company_1.refresh_from_db()
        self.assertEqual(self.company_1.description, "An updated description.")

    def test_admin_can_update_any_profile(self):
        """An admin user CAN update any company's profile."""
        self.client.force_authenticate(user=self.admin_user)
        update_data = {"is_active": True}
        response = self.client.patch(self.company_detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company_1.refresh_from_db()
        self.assertTrue(self.company_1.is_active)

    def test_unauthenticated_cannot_access(self):
        """Unauthenticated users cannot access company data."""
        response = self.client.get(self.company_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.patch(self.company_detail_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_company_uses_read_serializer(self):
        """The GET response should not contain sensitive write-only fields."""
        self.client.force_authenticate(user=self.company_user_1)
        response = self.client.get(self.my_company_url)
        # Check that a field from the read serializer is present
        self.assertIn("website", response.data)
        # The nested user object should also use the read serializer
        self.assertIn("get_full_name", response.data["user"])
        # Ensure a sensitive field from the UserSerializer is NOT present
        self.assertNotIn("password", response.data["user"])
