from rest_framework import serializers
from .models import Job, Application
from companies.serializers import CompanyReadSerializer
from seekers.serializers import SeekerProfileReadSerializer, ResumeReadSerializer

# --- Application Serializers ---

class ApplicationReadSerializer(serializers.ModelSerializer):
    """Serializer for reading application data with nested details."""
    applicant = SeekerProfileReadSerializer(read_only=True)
    resume = ResumeReadSerializer(read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'resume', 'cover_letter', 'applied_at', 'status']

class ApplicationWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating an application."""
    class Meta:
        model = Application
        fields = ['job', 'resume', 'cover_letter'] # Applicant is set from context

    def create(self, validated_data):
        # Automatically set the applicant from the request user's seeker profile.
        seeker_profile = self.context['request'].user.seekerprofile
        validated_data['applicant'] = seeker_profile
        return super().create(validated_data)

# --- Job Serializers ---

class JobReadSerializer(serializers.ModelSerializer):
    """Serializer for reading job data with nested company details."""
    company = CompanyReadSerializer(read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'company', 'salary', 'date_posted', 
            'last_date_to_apply', 'vacancy', 'employment_type'
        ]

class JobWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating a job."""
    class Meta:
        model = Job
        exclude = ['company'] # Company is set from context

    def create(self, validated_data):
        # Automatically set the company from the request user's company profile.
        company_profile = self.context['request'].user.company
        validated_data['company'] = company_profile
        return super().create(validated_data) 