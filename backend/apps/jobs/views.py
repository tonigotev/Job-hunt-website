from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Job, Application, Company
from .serializers import JobReadSerializer, JobWriteSerializer, ApplicationReadSerializer, ApplicationWriteSerializer
from core.permissions import IsOwnerOrReadOnly
from .permissions import IsAdminOrApplicationOwnerOrCompany

class JobsListPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'company__title', 'company__location']
    filterset_fields = ['employment_type', 'company__location']
    ordering_fields = ['salary', 'date_posted']
    pagination_class = JobsListPagination
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'my_jobs']:
            return JobReadSerializer
        return JobWriteSerializer

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

    @action(detail=False, methods=['get'], url_path='my-jobs', permission_classes=[permissions.IsAuthenticated])
    def my_jobs(self, request):
        if request.user.role != 'company':
            return Response({'detail': 'You are not authorized to view this page.'}, status=status.HTTP_403_FORBIDDEN)
        
        company = get_object_or_404(Company, user=request.user)
        jobs = Job.objects.filter(company=company)
        serializer = JobReadSerializer(jobs, many=True)
        return Response(serializer.data)

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrApplicationOwnerOrCompany]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job', 'status'] # Now you can filter by /api/jobs/applications/?job=1

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ApplicationReadSerializer
        return ApplicationWriteSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'company':
            return Application.objects.filter(job__company__user=user)
        elif user.role == 'job_seeker':
            return Application.objects.filter(applicant__user=user)
        return Application.objects.all() # For admins
