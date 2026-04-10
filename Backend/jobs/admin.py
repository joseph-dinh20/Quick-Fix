from django.contrib import admin
from .models import Job, JobImage, JobApplication

class JobImageInline(admin.TabularInline):
    model = JobImage
    extra = 1


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'budget', 'created_at', 'deadline', 'is_open', 'request_type')
    list_filter = ('is_open', 'request_type', 'created_at')
    search_fields = ('title', 'description', 'customer__user__username') 
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [JobImageInline]
    filter_horizontal = ('services',)  


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'provider', 'status')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)