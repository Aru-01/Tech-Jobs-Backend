from rest_framework import serializers
from accounts.models import User


from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "email", "profile_image", "role", "created_at")
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
    # We don't need to override much, dj-rest-auth handles email-only via settings
    pass

