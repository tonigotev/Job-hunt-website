from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'seekers'

router = DefaultRouter()
router.register(r'profiles', views.SeekerProfileViewSet, basename='seeker-profile')
router.register(r'resumes', views.ResumeViewSet, basename='resume')
router.register(r'experiences', views.ExperienceViewSet, basename='experience')

urlpatterns = [
    path('', include(router.urls)),
] 