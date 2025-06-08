from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Job, Application
from .permissions import IsCompanyOrAdmin, IsCompany, RoleBasedPermission

class JobsListPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = [IsAuthenticated, IsCompanyOrAdmin]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'company__location']
    filterset_fields = ['employment_type', 'salary']
    ordering_fields = ['salary', 'date_posted']
    ordering = ['-date_posted']
    pagination_class = JobsListPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        min_salary = self.request.query_params.get('min_salary', None)
        max_salary = self.request.query_params.get('max_salary', None)
        if min_salary:
            queryset = queryset.filter(salary__gte=min_salary)
        if max_salary:
            queryset = queryset.filter(salary__lte=max_salary)
        return queryset

class CompanyJobsView(APIView):
    permission_classes = [IsAuthenticated, IsCompany]

    def get(self, request):
        jobs = Job.objects.filter(company__user=request.user)
        serializer = serializers.JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def patch(self, request, pk=None):
        job = Job.objects.filter(company__user=request.user, pk=pk).first()
        if not job or job.company.user != request.user:
            raise PermissionDenied("You do not have permission to update this job.")

        serializer = serializers.JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('-id')
    serializer_class = serializers.ApplicationSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def get_queryset(self):
        user = self.request.user
        objects = super().get_queryset()

        if user.role == 'admin':
            return objects.all()

        elif user.role == 'company':
            return objects.filter(job__company__user=user)

        elif user.role == 'job_seeker':
            return objects.filter(applicant__user=user)

        return objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['GET'], permission_classes=[IsCompany])
    def list_by_job(self, request):
        job_id = request.query_params.get('jobID', None)
        if not job_id:
            return Response({"detail": "jobID parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        applications = self.get_queryset().filter(job__id=job_id)
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsCompany])
    def filter_applications(self, request):
        app_status = request.query_params.get('status')
        job_id = request.query_params.get('jobID')

        if not app_status or not job_id:
            return Response(
                {"detail": "Both jobID and status query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        applications = self.get_queryset().filter(job__id=job_id)
        if app_status != "all":
            applications = applications.filter(status=app_status)

        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
