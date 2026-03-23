from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("reporter", "reported_profile", "reason", "status", "created_at")
    list_filter = ("reason", "status", "created_at")
    search_fields = ("reporter__user__username", "reported_profile__user__username", "details")
    ordering = ("-created_at",)