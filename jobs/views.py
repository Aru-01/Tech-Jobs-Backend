from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Job
from .serializers import JobSerializer


class IsRecruiterOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ["admin", "recruiter"]
        )


class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.role == "admin" or obj.created_by == request.user)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterOrAdminOrReadOnly, IsAuthorOrAdmin]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Filter setup
    filterset_fields = ["job_type", "location", "experience_level"]

    # Search setup
    search_fields = ["title", "location", "company__company_name"]

    # Ordering setup
    ordering_fields = ["created_at", "salary"]

    @swagger_auto_schema(
        operation_description="List all jobs. Supports search (title, location, company), filters (job_type, location, experience_level), and ordering.",
        responses={200: JobSerializer(many=True)},
        tags=["Jobs"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new job post. Only Recruiters and Admins can create.",
        request_body=JobSerializer,
        responses={201: JobSerializer()},
        tags=["Jobs"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific job by ID.",
        responses={200: JobSerializer()},
        tags=["Jobs"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a job completely. Only the author or Admin can update.",
        request_body=JobSerializer,
        responses={200: JobSerializer()},
        tags=["Jobs"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a job. Only the author or Admin can update.",
        request_body=JobSerializer,
        responses={200: JobSerializer()},
        tags=["Jobs"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a job post. Only the author or Admin can delete.",
        responses={204: "No Content"},
        tags=["Jobs"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
