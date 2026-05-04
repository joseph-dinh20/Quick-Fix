from django.contrib import admin
from .models import Order


@admin.register(Order)
class JobAdmin(admin.ModelAdmin):
    list_display = ('customer', 'provider', 'amount', 'date_completed',)
    list_filter = ('date_completed',)
    search_fields = ('customer', 'provider',) 
    date_hierarchy = 'date_completed'
    ordering = ('-date_completed',)
