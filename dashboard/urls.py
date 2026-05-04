from django.urls import path
from .views import DashboardStatsView, MyJobsView, MyCompaniesView

urlpatterns = [
    path("stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("my-jobs/", MyJobsView.as_view(), name="my-jobs"),
    path("my-companies/", MyCompaniesView.as_view(), name="my-companies"),
]
