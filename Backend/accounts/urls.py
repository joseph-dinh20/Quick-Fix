from django.urls import path
from .views import signup, login, logout, csrf, me, get_providers, get_provider, update_profile, update_service_provider, delete_work_image, provider_me, get_services, update_provider_services

urlpatterns = [
    path("csrf/", csrf),
    path("signup/", signup),
    path("login/", login),
    path("logout/", logout),
    path("me/", me),
    path("providers/", get_providers),
    path("providers/<int:provider_id>/", get_provider),
    path("profile/update/", update_profile),
    path("provider/update/", update_service_provider),
    path("provider/work-images/<int:image_id>/delete/", delete_work_image),
    path("provider/me/", provider_me),
    path("services/", get_services, name="get_services"),
    path("provider/services/update/", update_provider_services, name="update_provider_services"),
]
