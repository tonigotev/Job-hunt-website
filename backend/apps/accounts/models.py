from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        JOB_SEEKER = 'job_seeker', 'Job Seeker'
        COMPANY = 'company', 'Company'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.JOB_SEEKER)
    email = models.EmailField(unique=True)