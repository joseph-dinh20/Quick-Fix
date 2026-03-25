from django.urls import path
from .views import create_review, get_reviews

urlpatterns = [
    path("<int:service_provider_id>/reviews/", get_reviews),
    path("<int:service_provider_id>/reviews/create/", create_review),
]