from django.urls import path
from rest_framework.routers import DefaultRouter
from companies.views import CompanyViewSet
from companies import views

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('user-company/', views.UserCompanyView.as_view()),
] + router.urls
