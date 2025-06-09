from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from . import serializers
from .models import Job, Application
from .permissions import IsAdminOrJobOwner, IsAdminOrApplicationOwnerOrCompany

class JobsListPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().select_related('company__user')
    permission_classes = [IsAuthenticated, IsAdminOrJobOwner]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'company__title', 'company__location']
    filterset_fields = ['employment_type', 'company__location']
    ordering_fields = ['salary', 'date_posted']
    pagination_class = JobsListPagination
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.JobReadSerializer
        return serializers.JobWriteSerializer

    def get_queryset(self):
        # Public 'list' and 'retrieve' actions can see all jobs
        if self.action in ['list', 'retrieve']:
            return Job.objects.all().select_related('company__user')
        
        # For actions requiring ownership, filter by the user's company
        if self.request.user.role == 'company':
            return Job.objects.filter(company__user=self.request.user)
        
        # Admins can see everything for ownership-based actions
        if self.request.user.role == 'admin':
            return Job.objects.all()

        return Job.objects.none()

    @action(detail=False, methods=['GET'], url_path='my-jobs')
    def my_jobs(self, request):
        """
        Retrieve all jobs for the currently authenticated company user.
        """
        if request.user.role != 'company':
            return Response({"detail": "You are not authorized to view this page."}, status=status.HTTP_403_FORBIDDEN)
        
        company_jobs = self.get_queryset()
        serializer = self.get_serializer(company_jobs, many=True)
        return Response(serializer.data)

class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrApplicationOwnerOrCompany]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job', 'status'] # Now you can filter by /api/jobs/applications/?job=1

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.ApplicationReadSerializer
        return serializers.ApplicationWriteSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Application.objects.all().select_related('applicant__user', 'job__company')
        if user.role == 'company':
            # Companies can only see applications for their own jobs
            return Application.objects.filter(job__company__user=user).select_related('applicant__user', 'job__company')
        if user.role == 'job_seeker':
            # Seekers can only see their own applications
            return Application.objects.filter(applicant__user=user).select_related('applicant__user', 'job__company')
        return Application.objects.none()
