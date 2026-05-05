from django.db.models import ImageField
from rest_framework import serializers
from accounts.models import User


from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(
        required=False, allow_null=True, allow_empty_file=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "profile_image",
            "profile_image_url",
            "role",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    full_name = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default="job_seeker")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            del self.fields["username"]

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["full_name"] = self.validated_data.get("full_name", "")
        data["role"] = self.validated_data.get("role", "job_seeker")
        return data

    def save(self, request):
        user = super().save(request)
        user.full_name = self.validated_data.get("full_name", "")
        user.role = self.validated_data.get("role", "job_seeker")
        user.save()
        return user


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            del self.fields["username"]

    def validate(self, attrs):
        # Map email to username for dj-rest-auth internal authentication logic
        if "email" in attrs:
            attrs["username"] = attrs.get("email")
        return super().validate(attrs)
