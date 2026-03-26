from django.urls import path
from .views import create_review, get_reviews, delete_review

urlpatterns = [
    path("<int:service_provider_id>/reviews/", get_reviews),
    path("<int:service_provider_id>/reviews/create/", create_review),
    path("delete/<int:review_id>/", delete_review),
]