from rest_framework import serializers

from accounts.serializers import UserSerializer
from companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Company
        fields = "__all__"

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

