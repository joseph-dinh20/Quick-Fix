from django.urls import path
from .views import update_job

urlpatterns = [
    path("<int:job_id>/edit/", update_job, name="update_job"),
]