from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'jobs'

router = DefaultRouter()
router.register(r'postings', views.JobViewSet, basename='job')
router.register(r'applications', views.ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]
