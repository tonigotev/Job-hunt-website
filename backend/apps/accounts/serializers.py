from django.contrib.auth import get_user_model
from rest_framework import serializers
from companies.models import Company
from seekers.models import SeekerProfile
import re

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'first_name', 'last_name', 'get_full_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'get_full_name': {'read_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'role': {'required': True}
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain letters, numbers, and underscores.")
        return value

    def validate(self, data):
        if data.get('role') not in ['job_seeker', 'company']:
            raise serializers.ValidationError({'role': 'Invalid role selected.'})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Create associated profile based on role
        if user.role == 'job_seeker':
            SeekerProfile.objects.create(user=user)
        elif user.role == 'company':
            Company.objects.create(
                user=user,
                title=f"{user.first_name} {user.last_name}'s Company",
                location='Not specified',
                description='Company description not provided yet.',
                is_active=True
            )
        return user
