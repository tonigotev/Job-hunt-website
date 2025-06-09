from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from companies.models import Company
from jobs.models import Job, Application
from seekers.models import SeekerProfile, Resume

User = get_user_model()


class JobsTests(APITestCase):
    def setUp(self):
        # Create Users
        self.company_user = User.objects.create_user(
            username="testcompany", password="Password123", role="company"
        )
        self.other_company_user = User.objects.create_user(
            username="othercompany", password="Password123", role="company"
        )
        self.seeker_user = User.objects.create_user(
            username="testseeker", password="Password123", role="job_seeker"
        )
        self.admin_user = User.objects.create_superuser(
            username="admin", password="Password123", role="admin"
        )

        # Get Company and Seeker Profiles
        self.company = Company.objects.get(user=self.company_user)
        self.seeker = SeekerProfile.objects.get(user=self.seeker_user)
        
        # Create a Resume for the seeker
        self.resume = Resume.objects.create(seeker=self.seeker, title="My Resume", file="path/to/resume.pdf")

        # Create a Job
        self.job = Job.objects.create(
            company=self.company, title="Software Engineer", salary=100000
        )

        # URLs
        self.jobs_url = reverse("jobs:job-list")
        self.job_detail_url = reverse("jobs:job-detail", kwargs={"pk": self.job.pk})
        self.applications_url = reverse("jobs:application-list")

    # --- JobViewSet Tests ---

    def test_company_can_create_job(self):
        """A company user should be able to create a job."""
        self.client.force_authenticate(user=self.company_user)
        job_data = {"title": "New Job", "description": "A great new job"}
        response = self.client.post(self.jobs_url, job_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 2)
        # Check the new job is correctly associated with the company
        new_job = Job.objects.get(pk=response.data['id'])
        self.assertEqual(new_job.company, self.company)

    def test_seeker_cannot_create_job(self):
        """A job seeker should NOT be able to create a job."""
        self.client.force_authenticate(user=self.seeker_user)
        job_data = {"title": "Seeker Job"}
        response = self.client.post(self.jobs_url, job_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_company_can_update_own_job(self):
        """A company should be able to update its own job."""
        self.client.force_authenticate(user=self.company_user)
        update_data = {"salary": 120000}
        response = self.client.patch(self.job_detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.job.refresh_from_db()
        self.assertEqual(self.job.salary, 120000)

    def test_company_cannot_update_other_job(self):
        """A company should NOT be able to update another company's job."""
        self.client.force_authenticate(user=self.other_company_user)
        update_data = {"salary": 999999}
        response = self.client.patch(self.job_detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    # --- ApplicationViewSet Tests ---
    
    def test_seeker_can_apply_for_job(self):
        """A job seeker should be able to apply for a job."""
        self.client.force_authenticate(user=self.seeker_user)
        application_data = {"job": self.job.pk, "resume": self.resume.pk, "cover_letter": "I am interested."}
        response = self.client.post(self.applications_url, application_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.get().applicant, self.seeker)

    def test_company_cannot_apply_for_job(self):
        """A company user should NOT be able to apply for a job."""
        self.client.force_authenticate(user=self.company_user)
        application_data = {"job": self.job.pk, "resume": self.resume.pk}
        response = self.client.post(self.applications_url, application_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_company_can_view_applications_for_own_job(self):
        """A company should be able to view applications for its own jobs."""
        Application.objects.create(job=self.job, applicant=self.seeker, resume=self.resume)
        self.client.force_authenticate(user=self.company_user)
        response = self.client.get(self.applications_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['applicant']['user']['username'], self.seeker_user.username)

    def test_company_cannot_view_applications_for_other_job(self):
        """A company should NOT see applications for other companies' jobs."""
        Application.objects.create(job=self.job, applicant=self.seeker, resume=self.resume)
        self.client.force_authenticate(user=self.other_company_user)
        response = self.client.get(self.applications_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
