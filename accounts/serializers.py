from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "email", "profile_image", "role", "created_at")
        read_only_fields = ("id", "created_at")
