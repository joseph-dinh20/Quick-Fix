from django.urls import path
from .views import signup, login, logout, csrf, me

urlpatterns = [
    path("csrf/", csrf),
    path("signup/", signup),
    path("login/", login),
    path("logout/", logout),
    path("me/", me),
]