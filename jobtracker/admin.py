from django.contrib import admin
from .models import Company, JobApplication, Position, JobType, Status

class JobApplicationAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Applicant Info", {
            "fields": ["user", "date_applied"]
        }),
        ("Job Details", {
            "fields": ["company", ("position", "job_type"), "job_link"]
        }),
        ("Application Status", {
            "fields": ["status", "notes"]
        }),
    ]
    list_display = ("user", "company", "position", "job_type", "status", "date_applied")
    search_fields = ("user__username", "company__name", "position__title")
    list_filter = ("status", "job_type", "company")


class CompanyAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Info", {
            "fields": ["name", "email", "phone_number"]
        }),
        ("Additional Details", {
            "fields": ["website", "description"]
        })
    ]
    list_display = ("name", "email", "phone_number")
    search_fields = ("name", "email")
    list_filter = ("name", "email", "phone_number")

admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Position)
admin.site.register(JobType)
admin.site.register(Status)
