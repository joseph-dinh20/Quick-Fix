from django.urls import path
from .views import create_review, get_reviews, delete_review, update_review, delete_review_image

urlpatterns = [
    path("provider/<int:service_provider_id>/", get_reviews),
    path("provider/<int:service_provider_id>/create/", create_review),

    path("<int:review_id>/delete/", delete_review),
    path("<int:review_id>/update/", update_review),

    path("images/<int:image_id>/delete/", delete_review_image),
]