from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .models import Company
from .permissions import IsAdminOrCompanyOwner


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrCompanyOwner]

    def get_serializer_class(self):
        if self.action == 'my_company' and self.request.method in ['GET', 'PATCH', 'PUT']:
             # Use the write serializer for updates, read for retrieval
            return serializers.CompanyReadSerializer if self.request.method == 'GET' else serializers.CompanySerializer
        elif self.action in ['retrieve', 'list']:
            return serializers.CompanyReadSerializer
        return serializers.CompanySerializer
        
    @action(detail=False, methods=['GET', 'PATCH', 'PUT'], url_path='my-company')
    def my_company(self, request):
        """
        Retrieve, update, or partially update the company profile of the request user.
        """
        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            return Response({"detail": "Company profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = self.get_serializer(company)
            return Response(serializer.data)

        elif request.method in ['PATCH', 'PUT']:
            serializer = self.get_serializer(company, data=request.data, partial=request.method == 'PATCH')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)