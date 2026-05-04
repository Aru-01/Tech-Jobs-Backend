from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from jobs.models import Job
from jobs.serializers import JobSerializer
from companies.models import Company
from companies.serializers import CompanySerializer


from rest_framework.views import APIView
from rest_framework.response import Response


class DashboardStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        active_jobs = Job.objects.count()
        companies_hiring = Company.objects.count()
        # Mocking these for now as per design
        return Response({
            "active_jobs": active_jobs,
            "companies_hiring": companies_hiring,
            "successful_hires": "98K+",
            "avg_time_to_hire": "18 days"
        })


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/api/auth/callback/google"  # Update with your frontend URL
    client_class = OAuth2Client


class MyJobsView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all jobs created by the currently authenticated user.",
        tags=["My Jobs"],
        responses={200: JobSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Job.objects.select_related("company", "created_by").filter(created_by=self.request.user)


class MyCompaniesView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all companies created by the currently authenticated user.",
        tags=["My Companies"],
        responses={200: CompanySerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Company.objects.select_related("created_by").filter(created_by=self.request.user)
