from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.db.models import Q
from collections import Counter
from drf_yasg.utils import swagger_auto_schema
from jobs.models import Job
from jobs.serializers import JobSerializer
from companies.models import Company
from companies.serializers import CompanySerializer

class DashboardStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        active_jobs = Job.objects.count()
        companies_hiring = Company.objects.count()

        # Truly dynamic tech stack counting
        # This will look at every item in the tech_stack list for all jobs
        all_tech_stacks = Job.objects.values_list('tech_stack', flat=True)
        
        # Flatten the list of lists and count occurrences
        tech_counter = Counter()
        for stack in all_tech_stacks:
            if isinstance(stack, list):
                tech_counter.update(stack)
            elif isinstance(stack, str):
                # Fallback if tech_stack was somehow stored as a string instead of a list
                tech_counter.update([stack])

        # Convert counter to the requested format: [{'label': 'React', 'count': 5}, ...]
        results = [
            {'label': tech, 'count': count} 
            for tech, count in tech_counter.items()
        ]

        # Add common categories as well by checking keywords in title or tech_stack
        # This keeps the high-level categories while the tech items are dynamic
        categories = ['Frontend', 'Backend', 'DevOps', 'AI / ML', 'UI / UX', 'Mobile', 'Cloud']
        for cat in categories:
            count = Job.objects.filter(
                Q(title__icontains=cat) | Q(tech_stack__icontains=cat)
            ).count()
            if count > 0:
                # Avoid duplicates if a category name is also a tech stack item
                if not any(r['label'] == cat for r in results):
                    results.append({'label': cat, 'count': count})

        # Add Remote Jobs
        remote_count = Job.objects.filter(location__icontains='Remote').count()
        results.append({'label': 'Remote Jobs', 'count': remote_count})

        # Sort by count descending and take top 15 to keep dashboard clean
        results.sort(key=lambda x: x['count'], reverse=True)
        top_results = results[:15]

        return Response({
            "active_jobs": active_jobs,
            "companies_hiring": companies_hiring,
            "successful_hires": "10+",
            "avg_time_to_hire": "05 days",
            "specialties": top_results
        })

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
        return Job.objects.select_related("company", "created_by").filter(
            created_by=self.request.user
        )

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
        return Company.objects.select_related("created_by").filter(
            created_by=self.request.user
        )
