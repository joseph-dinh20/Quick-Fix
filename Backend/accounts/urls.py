from django.urls import path
from .views import signup, login, logout, csrf, me, get_providers, get_provider

urlpatterns = [
    path("csrf/", csrf),
    path("signup/", signup),
    path("login/", login),
    path("logout/", logout),
    path("me/", me),
    path("providers/", get_providers),
    path("providers/<int:provider_id>/", get_provider),
]