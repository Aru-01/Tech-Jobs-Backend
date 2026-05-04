from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'industry', 'location', 'website', 'created_at')
    search_fields = ('company_name', 'industry', 'location')
    list_filter = ('industry', 'location', 'created_at')
