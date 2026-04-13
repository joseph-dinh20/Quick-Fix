from django.urls import path
from .views import create_job, my_jobs, get_favorites, toggle_favorite, list_jobs, delete_job, update_job, search_jobs
from .views import my_applications, apply_to_job, accept_application, complete_job, get_assigned_jobs, delete_job_image

urlpatterns = [
    path("create/", create_job),
    path("mine/", my_jobs),
    path("favorites/", get_favorites),
    path("<int:job_id>/favorite/", toggle_favorite),
    path("", list_jobs),    
    path("<int:job_id>/delete/", delete_job),
    path("<int:job_id>/edit/", update_job, name="update_job"),
    path("search/", search_jobs, name="search_job"),
    path("my-applications/", my_applications),
    path("<int:job_id>/apply/", apply_to_job),
    path("applications/<int:application_id>/accept/", accept_application),
    path("<int:job_id>/complete/", complete_job),
    path("assigned/", get_assigned_jobs),
    path("images/<int:image_id>/delete/", delete_job_image)
]