from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "role", "price_per_hour")
    search_fields = ("name", "user__username")
    list_filter = ("role",)

