from django.db import models
from django.conf import settings
from companies.models import Company

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    )

    EXPERIENCE_LEVEL_CHOICES = (
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('director', 'Director'),
    )

    title = models.CharField(max_length=255)
    short_description = models.TextField()
    full_description = models.TextField()
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES)
    deadline = models.DateField()
    tech_stack = models.JSONField(default=list, help_text="List of technologies (e.g. ['python', 'django'])")
    banner_image_url = models.URLField(max_length=500, blank=True, null=True)
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_jobs')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
