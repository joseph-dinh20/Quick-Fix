from django.urls import path
from .views import create_review, get_reviews, delete_review, update_review, delete_review_image

urlpatterns = [
    path("<int:service_provider_id>/reviews/", get_reviews),
    path("<int:service_provider_id>/reviews/create/", create_review),
    path("delete/<int:review_id>/", delete_review),
    path("update/<int:review_id>/", update_review),
    path("images/<int:image_id>/delete/", delete_review_image)
]