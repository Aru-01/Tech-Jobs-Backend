import json
from rest_framework import serializers
from django.utils import timezone
from .models import Job
from companies.serializers import CompanySerializer


class JobSerializer(serializers.ModelSerializer):
    company_details = CompanySerializer(source="company", read_only=True)
    banner_image = serializers.ImageField(
        required=False, allow_null=True, allow_empty_file=True
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "short_description",
            "full_description",
            "salary",
            "location",
            "job_type",
            "experience_level",
            "deadline",
            "tech_stack",
            "banner_image",
            "banner_image_url",
            "company",
            "company_details",
            "created_by",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = ("id", "created_by", "created_at", "updated_at", "is_active")

    tech_stack = serializers.CharField(required=False, allow_blank=True)

    def validate_tech_stack(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value

        try:
            # Attempt to parse as JSON first
            result = json.loads(value)
            if isinstance(result, list):
                return [str(t) for t in result if t is not None]
            return [str(result)]
        except (json.JSONDecodeError, TypeError):
            # Fallback to comma-separated string parsing
            if "," in value:
                return [t.strip() for t in value.split(",") if t.strip()]
            return [value.strip()] if value.strip() else []

    def to_internal_value(self, data):
        # We don't need a complex to_internal_value anymore since we're using CharField + validate_tech_stack
        return super().to_internal_value(data)

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value

    def validate_deadline(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value

    def validate(self, attrs):
        return attrs
