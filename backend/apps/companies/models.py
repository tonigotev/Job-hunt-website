from django.contrib.auth import get_user_model
from django.db import models

def standardize_location_name(location):
    return location.strip().title()


class Company(models.Model):
    title = models.CharField(max_length=150)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    location = models.CharField(max_length=150)
    description = models.TextField()
    website = models.URLField(null=True)
    established_date = models.DateField(null=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.location = standardize_location_name(self.location)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"