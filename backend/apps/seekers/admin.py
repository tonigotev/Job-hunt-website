from django.contrib import admin

from seekers.models import Resume, SeekerProfile, Experience

admin.site.register(SeekerProfile)
admin.site.register(Resume)
admin.site.register(Experience)
