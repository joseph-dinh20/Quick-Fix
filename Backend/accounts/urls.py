from django.urls import path
from .views import signup, login, logout, csrf, me
from .views import get_providers, get_provider
from .views import update_profile, update_service_provider, delete_work_image, provider_me, get_services, update_provider_services
from .views import get_favorites, toggle_favorite_provider, is_favorite_provider
from .views import get_nearby_providers, search_providers
from .views import apply_provider, update_provider_status

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
    path("providers/<int:provider_id>/favorite/", toggle_favorite_provider),
    path("providers/favorites/", get_favorites),
    path("providers/<int:provider_id>/is-favorite/", is_favorite_provider),
    path("providers/nearby/", get_nearby_providers),
    path("providers/search/", search_providers, name="search_provider"),
    path("provider/apply/", apply_provider),
    path("provider/<int:user_id>/status/", update_provider_status)

]