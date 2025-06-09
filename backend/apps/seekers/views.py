from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from seekers import serializers
from seekers.models import SeekerProfile, Experience, Resume
from seekers.permissions import IsAdminOrOwner
from .permissions import IsAdminOrOwner


class SeekerProfileViewSet(viewsets.ModelViewSet):
    queryset = SeekerProfile.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    # based on the action, we will return the appropriate serializer so we don't expose all fields
    def get_serializer_class(self):
        if self.action in ['retrieve', 'list'] or (self.action == 'my_profile' and self.request.method == 'GET'):
            return serializers.SeekerProfileReadSerializer
        return serializers.SeekerProfileSerializer

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        obj, created = SeekerProfile.objects.get_or_create(user=request.user)

        if request.method == 'GET':
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        return Resume.objects.filter(seeker__user=self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return serializers.ResumeReadSerializer
        return serializers.ResumeSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        return Experience.objects.filter(seeker__user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return serializers.ExperienceReadSerializer
        return serializers.ExperienceSerializer
