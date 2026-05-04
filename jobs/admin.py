from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'experience_level', 'salary', 'deadline', 'created_at')
    search_fields = ('title', 'company__company_name', 'location')
    list_filter = ('job_type', 'experience_level', 'created_at')
