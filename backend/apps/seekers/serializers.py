from datetime import datetime

from rest_framework import serializers

from accounts.serializers import UserReadSerializer, UserSerializer
from seekers.models import SeekerProfile, Resume, Experience


class SeekerProfileReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading SeekerProfile data, using a nested UserReadSerializer.
    """
    user = UserReadSerializer()

    class Meta:
        model = SeekerProfile
        fields = ['user', 'bio', 'profile_photo']


class SeekerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = SeekerProfile
        fields = "__all__"

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ResumeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'resume_title', 'resume', 'date_created']


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"
        read_only_fields = ['seeker']

    def create(self, validated_data):
        validated_data['seeker'] = SeekerProfile.objects.get(user=self.context['request'].user)
        return super().create(validated_data)


class MonthField(serializers.DateField):
    def to_internal_value(self, value):
        try:
            return datetime.strptime(f"{value}-01", "%Y-%m-%d").date()
        except ValueError:
            raise serializers.ValidationError("Invalid month format. Expected 'YYYY-MM'.")

    def to_representation(self, value):
        return value.strftime("%Y-%m")


class ExperienceReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'job_title', 'company', 'start_date', 'end_date', 'is_current']


class ExperienceSerializer(serializers.ModelSerializer):
    start_date = MonthField()
    end_date = MonthField()

    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = ['seeker']

    def create(self, validated_data):
        validated_data['seeker'] = SeekerProfile.objects.get(user=self.context['request'].user)
        return super().create(validated_data)
