from rest_framework import serializers

from accounts.serializers import UserReadSerializer
from companies.models import Company


class CompanyReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()

    class Meta:
        model = Company
        fields = [
            'id', 'title', 'user', 'location', 'description', 
            'website', 'established_date', 'is_active'
        ]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

