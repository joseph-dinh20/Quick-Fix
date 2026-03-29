# services/admin.py
from django.contrib import admin
from .models import Review, ReviewImage
from accounts.models import ServiceProvider


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "reviewer", "service_provider", "rating", "created_at")
    list_filter = ("rating", "created_at", "service_provider")
    search_fields = ("reviewer__user__username", "service_provider__profile__name", "comment")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    inlines = [ReviewImageInline]