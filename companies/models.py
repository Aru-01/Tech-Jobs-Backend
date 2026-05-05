from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    logo = CloudinaryField("companies/logos/", blank=True, null=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    banner_image = CloudinaryField("companies/banners/", blank=True, null=True)
    banner_image_url = models.URLField(max_length=500, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    short_description = models.TextField()
    full_description = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="companies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.company_name
