from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import MyJobsView, MyCompaniesView, DashboardStatsView

schema_view = get_schema_view(
    openapi.Info(
        title="Tech Jobs API",
        default_version="v1",
        description="API documentation for Tech Jobs Job Portal",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@techjobs.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/companies/", include("companies.urls")),
    path("api/jobs/", include("jobs.urls")),
    path("api/my/jobs/", MyJobsView.as_view(), name="my-jobs"),
    path("api/my/companies/", MyCompaniesView.as_view(), name="my-companies"),
    path("api/dashboard/stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    # Swagger urls
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
