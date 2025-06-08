from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()


class AccountsTests(APITestCase):
    def setUp(self):
        # Base user data
        self.seeker_data = {
            "username": "testseeker",
            "email": "seeker@example.com",
            "password": "ValidPassword123",
            "first_name": "Test",
            "last_name": "Seeker",
            "role": "job_seeker",
        }
        self.company_data = {
            "username": "testcompany",
            "email": "company@example.com",
            "password": "ValidPassword123",
            "first_name": "Test",
            "last_name": "Company",
            "role": "company",
        }
        self.signup_url = reverse("accounts:signup")
        self.login_url = reverse("accounts:login")

    # --- Signup Tests ---
    def test_seeker_signup_successful(self):
        response = self.client.post(self.signup_url, self.seeker_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().role, "job_seeker")

    def test_company_signup_successful(self):
        response = self.client.post(self.signup_url, self.company_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().role, "company")

    def test_signup_duplicate_email_fails(self):
        self.client.post(self.signup_url, self.seeker_data, format="json")  # First user
        invalid_data = self.company_data.copy()
        invalid_data["email"] = self.seeker_data["email"]  # Duplicate email
        response = self.client.post(self.signup_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_signup_weak_password_fails(self):
        invalid_data = self.seeker_data.copy()
        invalid_data["password"] = "weak"
        response = self.client.post(self.signup_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_signup_invalid_role_fails(self):
        invalid_data = self.seeker_data.copy()
        invalid_data["role"] = "invalid_role"
        response = self.client.post(self.signup_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("role", response.data)
        
    # --- Login Tests ---
    def test_login_successful_with_username(self):
        self.client.post(self.signup_url, self.seeker_data, format="json")
        login_data = {"username": self.seeker_data["username"], "password": self.seeker_data["password"]}
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data['user']['email'], self.seeker_data['email'])

    def test_login_successful_with_email(self):
        self.client.post(self.signup_url, self.seeker_data, format="json")
        login_data = {"username": self.seeker_data["email"], "password": self.seeker_data["password"]}
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_wrong_password_fails(self):
        self.client.post(self.signup_url, self.seeker_data, format="json")
        login_data = {"username": self.seeker_data["username"], "password": "WrongPassword123"}
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- User Detail and Update Tests ---
    def test_get_user_detail_successful(self):
        self.client.post(self.signup_url, self.seeker_data, format="json")
        login_response = self.client.post(self.login_url, {"username": self.seeker_data["username"], "password": self.seeker_data["password"]})
        token = login_response.data['access']
        
        detail_url = reverse("accounts:user_detail")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.seeker_data["email"])

    def test_get_user_detail_unauthenticated_fails(self):
        detail_url = reverse("accounts:user_detail")
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_user_detail_successful(self):
        # Create and log in user
        self.client.post(self.signup_url, self.seeker_data, format="json")
        login_resp = self.client.post(self.login_url, {"username": self.seeker_data['username'], "password": self.seeker_data['password']})
        token = login_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Update user's first name
        update_url = reverse("accounts:user_update")
        update_data = {"first_name": "Updated"}
        response = self.client.patch(update_url, update_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")

        # Verify the change in the database
        user = User.objects.get(email=self.seeker_data['email'])
        self.assertEqual(user.first_name, "Updated")

    # --- Logout Test ---
    def test_logout_successful(self):
        self.client.post(self.signup_url, self.seeker_data, format="json")
        login_response = self.client.post(self.login_url, {"username": self.seeker_data["username"], "password": self.seeker_data["password"]})
        refresh_token = login_response.data['refresh']
        
        logout_url = reverse("accounts:logout")
        response = self.client.post(logout_url, {"refresh": refresh_token}, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Optional: Verify token is blacklisted by trying to use it again (requires more setup)
        # For simplicity, we trust the 200 OK response indicates success.
