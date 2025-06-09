from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from seekers import serializers
from seekers.models import SeekerProfile, Experience, Resume
from core.permissions import IsOwnerOrReadOnly


class SeekerProfileViewSet(viewsets.ModelViewSet):
    queryset = SeekerProfile.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list'] or (self.action == 'my_profile' and self.request.method == 'GET'):
            return serializers.SeekerProfileReadSerializer
        return serializers.SeekerProfileSerializer

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[permissions.IsAuthenticated], url_path='my-profile')
    def my_profile(self, request):
        profile = get_object_or_404(SeekerProfile, user=request.user)
        if request.method == 'GET':
            serializer = serializers.SeekerProfileReadSerializer(profile)
            return Response(serializer.data)
        
        serializer = serializers.SeekerProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResumeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Resume.objects.all()

    def get_queryset(self):
        return Resume.objects.filter(seeker__user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return serializers.ResumeReadSerializer
        return serializers.ResumeSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Experience.objects.all()

    def get_queryset(self):
        return Experience.objects.filter(seeker__user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return serializers.ExperienceReadSerializer
        return serializers.ExperienceSerializer
