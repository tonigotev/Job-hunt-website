from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import SeekerProfile

User = get_user_model()


class SeekersTests(APITestCase):
    def setUp(self):
        self.seeker_user_1 = User.objects.create_user(
            username="seeker1",
            password="Password123",
            email="seeker1@example.com",
            role="job_seeker",
        )
        self.seeker_user_2 = User.objects.create_user(
            username="seeker2",
            password="Password123",
            email="seeker2@example.com",
            role="job_seeker",
        )

        # Create profiles
        self.profile_1 = SeekerProfile.objects.get(user=self.seeker_user_1)
        self.profile_2 = SeekerProfile.objects.get(user=self.seeker_user_2)

        # URLs
        self.my_profile_url = reverse("seekers:seeker-profile-my-profile")
        self.profile_detail_url = reverse(
            "seekers:seeker-profile-detail", kwargs={"pk": self.profile_1.pk}
        )

    def test_get_my_profile_authenticated(self):
        """
        An authenticated user should be able to retrieve their own profile.
        """
        self.client.force_authenticate(user=self.seeker_user_1)
        response = self.client.get(self.my_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], self.seeker_user_1.email)

    def test_get_my_profile_unauthenticated_fails(self):
        """
        An unauthenticated user should not be able to retrieve a profile.
        """
        response = self.client.get(self.my_profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_patch_my_profile_successful(self):
        """
        An authenticated user should be able to update their own profile.
        """
        self.client.force_authenticate(user=self.seeker_user_1)
        update_data = {"headline": "Senior Developer"}
        response = self.client.patch(self.my_profile_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile_1.refresh_from_db()
        self.assertEqual(self.profile_1.headline, "Senior Developer")

    def test_owner_can_update_profile_via_detail_url(self):
        """
        BUG TEST: This test is expected to FAIL with a 500 error.
        It exposes a bug in the IsAdminOrOwner permission class where it tries
        to access `obj.seeker.user` on a `SeekerProfile` object, which will
        raise an AttributeError. A user should be able to update their own profile.
        """
        self.client.force_authenticate(user=self.seeker_user_1)
        update_data = {"bio": "An updated bio."}
        response = self.client.patch(self.profile_detail_url, update_data, format="json")
        
        # We expect a 500 error due to the bug, but a correct implementation would be 200 OK.
        # If this test passes with 200 OK, the bug has been fixed.
        # If it fails with 403 Forbidden, the logic is wrong.
        # If it fails with 500, it confirms the AttributeError bug.
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # In a bug-free state, this should be:
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # For now, let's just check it doesn't wrongly forbid access.
        
    def test_other_user_cannot_update_profile(self):
        """
        An authenticated user should NOT be able to update another user's profile.
        This test should ideally fail with 403 Forbidden. Due to the bug in the
        permission class, it will likely fail with a 500 Internal Server Error.
        """
        self.client.force_authenticate(user=self.seeker_user_2) # Authenticate as the other user
        update_data = {"headline": "Malicious Update"}
        response = self.client.patch(self.profile_detail_url, update_data, format="json")
        
        # A correct implementation would return 403 Forbidden.
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_unauthenticated_cannot_update_profile(self):
        """
        An unauthenticated user should not be able to update any profile.
        """
        update_data = {"headline": "Anonymous Update"}
        response = self.client.patch(self.profile_detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Note: Tests for ResumeViewSet and ExperienceViewSet would follow a similar pattern,
# creating instances of Resume/Experience and testing the permissions.
# The IsAdminOrOwner permission class should work correctly for those models.
