from rest_framework import serializers
from companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(
        required=False, allow_null=True, allow_empty_file=True
    )
    banner_image = serializers.ImageField(
        required=False, allow_null=True, allow_empty_file=True
    )

    class Meta:
        model = Company
        fields = [
            "id",
            "company_name",
            "logo",
            "logo_url",
            "banner_image",
            "banner_image_url",
            "website",
            "location",
            "industry",
            "short_description",
            "full_description",
            "is_verified",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_by", "created_at", "updated_at")
