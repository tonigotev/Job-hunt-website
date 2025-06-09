from rest_framework import serializers

from accounts.serializers import UserReadSerializer
from companies.models import Company


class CompanyReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Company data, ensuring only safe fields are exposed.
    """
    user = UserReadSerializer()

    class Meta:
        model = Company
        fields = [
            'id', 'title', 'user', 'location', 'description', 
            'website', 'established_date', 'is_active'
        ]


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for writing/updating Company data.
    """
    class Meta:
        model = Company
        # Exclude user field as it's set automatically from the request context.
        exclude = ['user']

    def create(self, validated_data):
        # The user is automatically assigned based on the authenticated request user.
        # This prevents a user from creating a company profile for someone else.
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

