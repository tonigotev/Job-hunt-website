from rest_framework import serializers
from .models import Job, Application
from companies.serializers import CompanyReadSerializer
from seekers.serializers import SeekerProfileReadSerializer, ResumeReadSerializer, ExperienceReadSerializer
from seekers.models import Resume, Experience
from django.db import IntegrityError


class JobReadSerializer(serializers.ModelSerializer):
    company = CompanyReadSerializer(read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'company', 'salary', 'date_posted', 
            'last_date_to_apply', 'vacancy', 'employment_type'
        ]

class JobWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ['company']

    def create(self, validated_data):
        company_profile = self.context['request'].user.company
        validated_data['company'] = company_profile
        return super().create(validated_data) 

class ApplicationReadSerializer(serializers.ModelSerializer):
    job = JobReadSerializer(read_only=True)
    applicant = SeekerProfileReadSerializer(read_only=True)
    resume = ResumeReadSerializer(read_only=True)
    experience = ExperienceReadSerializer(read_only=True)

    resume_url = serializers.FileField(source='resume.resume', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'applicant',
            'resume',
            'experience',
            'resume_url',
            'cover_letter',
            'applied_at',
            'status',
        ]

class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']

class ApplicationWriteSerializer(serializers.ModelSerializer):

    resume_id = serializers.IntegerField(write_only=True, required=False)
    experience_id = serializers.IntegerField(write_only=True, required=False)

    resume = serializers.FileField(write_only=True, required=False)
    resume_title = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Application
        fields = ['job', 'cover_letter', 'resume_id', 'resume', 'resume_title', 'experience_id']

    def create(self, validated_data):
        seeker_profile = self.context['request'].user.seekerprofile
        
        # --- Decide which resume to attach ---
        if resume_id := validated_data.pop('resume_id', None):
            # Using an existing resume
            resume_obj = Resume.objects.filter(id=resume_id, seeker=seeker_profile).first()
            if resume_obj is None:
                raise serializers.ValidationError("Invalid resume_id or you do not own this resume.")
        else:
            # Expecting an uploaded file + title
            uploaded_file = validated_data.pop('resume', None)
            title = validated_data.pop('resume_title', None)
            if not uploaded_file or not title:
                raise serializers.ValidationError("Provide either resume_id or both resume and resume_title.")

            resume_obj = Resume.objects.create(
                seeker=seeker_profile,
                resume_title=title,
                resume=uploaded_file,
            )

        # --- Attach experience ---
        experience_obj = None
        if exp_id := validated_data.pop('experience_id', None):
            experience_obj = Experience.objects.filter(id=exp_id, seeker=seeker_profile).first()
            if experience_obj is None:
                raise serializers.ValidationError("Invalid experience_id or you do not own this experience.")

        try:
            application = Application.objects.create(
                job=validated_data['job'],
                applicant=seeker_profile,
                cover_letter=validated_data.get('cover_letter', ''),
                resume=resume_obj,
                experience=experience_obj,
            )
        except IntegrityError:
            raise serializers.ValidationError("You have already applied for this job.")

        return application

