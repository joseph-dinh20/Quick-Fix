from django.urls import path
from .views import create_job, my_jobs, get_favorites, toggle_favorite, list_jobs, delete_job, update_job, search_jobs

urlpatterns = [
    path("create/", create_job),
    path("mine/", my_jobs),
    path("favorites/", get_favorites),
    path("<int:job_id>/favorite/", toggle_favorite),
    path("", list_jobs),    
    path("<int:job_id>/delete/", delete_job),
    path("<int:job_id>/edit/", update_job, name="update_job"),
    path("search/", search_jobs, name="search_job"),
]