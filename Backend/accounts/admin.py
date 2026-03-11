from django.contrib import admin
from .models import Profile, ServiceProvider, WorkImage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "role")  # user is fine here
    search_fields = ("name", "user__username", "user__email")
    list_filter = ("role",)

class WorkImageInline(admin.TabularInline):
    model = WorkImage
    extra = 1

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ("profile_name", "profile_email", "price_per_hour", "average_rating", "total_rating")
    search_fields = ("profile__name", "profile__user__username", "profile__user__email")
    filter_horizontal = ("services",)
    inlines = [WorkImageInline]
    
    def profile_name(self, obj):
        return obj.profile.name
    profile_name.short_description = "Name"

    def profile_email(self, obj):
        return obj.profile.user.email
    profile_email.short_description = "Email"