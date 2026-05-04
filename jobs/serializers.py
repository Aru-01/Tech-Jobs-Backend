from rest_framework import serializers
from django.utils import timezone
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'short_description', 'full_description', 
            'salary', 'location', 'job_type', 'experience_level', 
            'deadline', 'tech_stack', 'banner_image', 'banner_image_url', 
            'company', 'created_by', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at', 'is_active')

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value

    def validate_deadline(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value

    def validate(self, attrs):
        # Additional custom validation if necessary
        return attrs
