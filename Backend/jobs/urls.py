from django.urls import path
from .views import create_job, my_jobs

urlpatterns = [
    path("create/", create_job),
    path("mine/", my_jobs)
]